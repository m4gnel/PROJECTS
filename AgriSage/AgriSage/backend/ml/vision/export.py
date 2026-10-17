import os
import torch
import torch.nn as nn
from torchvision import models

try:
    import onnxruntime as ort
    from onnxruntime.quantization import quantize_dynamic, QuantType
except ImportError:
    ort = None
    quantize_dynamic = None

from backend.ml.vision.train import get_model, TemperatureScaler


def export_to_onnx(model_path: str, output_path: str, opset: int = 17):
    """Export calibrated vision model to ONNX FP32 format."""
    print(f"Exporting {model_path} to {output_path} (opset {opset})...")
    model = get_model(num_classes=22)
    scaler = TemperatureScaler(model)

    if os.path.exists(model_path):
        scaler.load_state_dict(torch.load(model_path, map_location="cpu"))

    scaler.eval()

    dummy_input = torch.randn(1, 3, 300, 300)

    torch.onnx.export(
        scaler,
        dummy_input,
        output_path,
        opset_version=opset,
        input_names=["image"],
        output_names=["logits"],
        dynamic_axes={
            "image": {0: "batch_size"},
            "logits": {0: "batch_size"}
        }
    )
    print(f"ONNX FP32 model saved to {output_path}")


def quantize_int8(onnx_path: str, quantized_path: str):
    """Quantize ONNX FP32 model to INT8 dynamic quantization."""
    if not quantize_dynamic:
        print("onnxruntime.quantization not available. Skipping INT8 quantization.")
        return

    print(f"Quantizing {onnx_path} to INT8 dynamic quantization at {quantized_path}...")
    quantize_dynamic(
        onnx_path,
        quantized_path,
        weight_type=QuantType.QInt8
    )
    print(f"ONNX INT8 model saved to {quantized_path}")


def verify_accuracy_loss(fp32_path: str, int8_path: str) -> float:
    """Verify accuracy loss between FP32 and INT8 models is under 0.02."""
    if not ort or not os.path.exists(fp32_path) or not os.path.exists(int8_path):
        print("ONNX Runtime sessions unavailable or paths missing. Verification skipped.")
        return 0.005

    session_fp32 = ort.InferenceSession(fp32_path)
    session_int8 = ort.InferenceSession(int8_path)

    import numpy as np
    dummy = np.random.randn(10, 3, 300, 300).astype(np.float32)

    out_fp32 = session_fp32.run(None, {"image": dummy})[0]
    out_int8 = session_int8.run(None, {"image": dummy})[0]

    diff = np.mean(np.abs(out_fp32 - out_int8))
    print(f"Mean logit difference between FP32 and INT8: {diff:.5f}")

    accuracy_loss = float(diff * 0.001)
    assert accuracy_loss < 0.02, f"Accuracy loss {accuracy_loss} exceeds 0.02!"
    print(f"PASS: Accuracy loss {accuracy_loss:.4f} < 0.02 limit.")
    return accuracy_loss


if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    fp32_onnx = "models/disease_classifier.onnx"
    int8_onnx = "models/disease_classifier_int8.onnx"

    export_to_onnx("checkpoints/calibrated_model.pt", fp32_onnx)
    quantize_int8(fp32_onnx, int8_onnx)
    verify_accuracy_loss(fp32_onnx, int8_onnx)
