"""
config.py — Centralised configuration loader.
Reads configs/config.yaml and provides typed access to every setting.
Unknown YAML keys are silently accepted via setattr, so adding new keys
to config.yaml never breaks this file.
"""
import os
from dataclasses import dataclass, field
from typing import Optional

import yaml


@dataclass
class DataConfig:
    train_dir:  str = "dataset/train"
    test_dir:   str = "dataset/test"
    output_dir: str = "output"


@dataclass
class NormalizationConfig:
    abbreviation_file: str = "configs/abbreviations.json"
    unicode_form:      str = "NFC"
    max_text_length:   int = 500


@dataclass
class EmbeddingConfig:
    model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    batch_size: int = 128
    device:     str = "cpu"
    enabled:    bool = False   # disabled by default — 37 GB RAM needed for full dataset


@dataclass
class BlockingConfig:
    tfidf_top_k:           int   = 20
    ngram_min_sim:         float = 0.15
    max_candidates_per_s1: int   = 100
    ngram_size:            int   = 3
    chunk_size:            int   = 50_000   # S1 rows per TF-IDF blocking chunk
    use_cache:             bool  = True     # cache intermediate results to disk


@dataclass
class MatchingConfig:
    model_type:           str   = "lightgbm"
    n_estimators:         int   = 1000
    learning_rate:        float = 0.05
    max_depth:            int   = 8
    num_leaves:           int   = 63
    threshold:            float = 0.5        # overwritten by val-set calibration
    hard_negative_ratio:  int   = 5
    random_negative_ratio: int  = 2
    random_seed:          int   = 42
    n_jobs:               int   = -1         # use all CPU cores
    subsample:            float = 0.8
    colsample_bytree:     float = 0.8


@dataclass
class ValidationConfig:
    split_ratio:      float = 0.2
    random_seed:      int   = 42
    val_sample_size:  int   = 20_000   # validate on 20k S1 entities (faster)


@dataclass
class Config:
    data:          DataConfig          = field(default_factory=DataConfig)
    normalization: NormalizationConfig = field(default_factory=NormalizationConfig)
    embedding:     EmbeddingConfig     = field(default_factory=EmbeddingConfig)
    blocking:      BlockingConfig      = field(default_factory=BlockingConfig)
    matching:      MatchingConfig      = field(default_factory=MatchingConfig)
    validation:    ValidationConfig    = field(default_factory=ValidationConfig)


def load_config(config_path: str = "configs/config.yaml") -> Config:
    """
    Load configuration from YAML file.
    Falls back to dataclass defaults if the file is missing.
    Any YAML key not defined in the dataclass is accepted silently via setattr.
    """
    config = Config()

    if not os.path.exists(config_path):
        print(f"[WARN] Config not found at '{config_path}' — using defaults.")
        return config

    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if not raw:
        return config

    section_map = {
        "data":          config.data,
        "normalization": config.normalization,
        "embedding":     config.embedding,
        "blocking":      config.blocking,
        "matching":      config.matching,
        "validation":    config.validation,
    }
    for section_name, target in section_map.items():
        if section_name in raw and raw[section_name]:
            for k, v in raw[section_name].items():
                setattr(target, k, v)   # unknown keys are fine

    return config
