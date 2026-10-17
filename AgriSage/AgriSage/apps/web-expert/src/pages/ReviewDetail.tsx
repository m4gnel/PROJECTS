import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

export default function ReviewDetail() {
  const { advisory_id } = useParams<{ advisory_id: string }>();
  const navigate = useNavigate();

  const [verdict, setVerdict] = useState("correct");
  const [correctedDiagnosis, setCorrectedDiagnosis] = useState("");
  const [notes, setNotes] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => {
      navigate("/dashboard");
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <button
        onClick={() => navigate("/dashboard")}
        className="mb-6 text-sm text-gray-400 hover:text-white"
      >
        ← Back to Queue
      </button>

      <h1 className="text-2xl font-bold text-green-400 mb-6">
        Advisory Review: {advisory_id}
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left column: Evidence bundle display */}
        <div className="space-y-6 bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 className="text-lg font-semibold text-gray-200">AI Generated Diagnosis</h2>
          <div className="bg-gray-900 p-4 rounded text-sm space-y-2">
            <p><span className="text-gray-400">Diagnosis:</span> Rice Blast (Magnaporthe oryzae)</p>
            <p><span className="text-gray-400">Confidence:</span> POSSIBLE (68%)</p>
            <p><span className="text-gray-400">DFI Index:</span> 0.78 (High moisture favorability)</p>
            <p><span className="text-gray-400">Crop Stage:</span> Tillering (Day 40)</p>
          </div>

          <h3 className="font-semibold text-sm text-gray-300">Evidence Chunks</h3>
          <ul className="list-disc list-inside text-xs text-gray-400 space-y-1">
            <li>ICAR Extension Leaflet: Blast control in Kharif paddy</li>
            <li>Open-Meteo 7-day relative humidity average &gt; 80%</li>
          </ul>
        </div>

        {/* Right column: Verdict Form */}
        <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 className="text-lg font-semibold text-gray-200 mb-4">Expert Verdict</h2>

          {submitted ? (
            <div className="p-4 bg-green-900/50 text-green-300 rounded text-center">
              ✓ Review submitted successfully! Returning to queue...
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs uppercase text-gray-400 font-semibold mb-1">
                  Verdict
                </label>
                <select
                  value={verdict}
                  onChange={(e) => setVerdict(e.target.value)}
                  className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white"
                >
                  <option value="correct">Correct</option>
                  <option value="partially_correct">Partially Correct</option>
                  <option value="incorrect">Incorrect</option>
                  <option value="insufficient_data">Insufficient Data</option>
                </select>
              </div>

              {verdict !== "correct" && (
                <div>
                  <label className="block text-xs uppercase text-gray-400 font-semibold mb-1">
                    Corrected Diagnosis / Recommendation
                  </label>
                  <input
                    type="text"
                    required
                    value={correctedDiagnosis}
                    onChange={(e) => setCorrectedDiagnosis(e.target.value)}
                    placeholder="Enter correct diagnosis or treatment"
                    className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white outline-none"
                  />
                </div>
              )}

              <div>
                <label className="block text-xs uppercase text-gray-400 font-semibold mb-1">
                  Expert Notes
                </label>
                <textarea
                  rows={4}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Additional notes for model fine-tuning"
                  className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white outline-none"
                />
              </div>

              <button
                type="submit"
                className="w-full bg-green-600 hover:bg-green-500 py-2 rounded font-bold text-white transition"
              >
                Submit Review Verdict
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
