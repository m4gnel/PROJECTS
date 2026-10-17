import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

interface QueueItem {
  advisory_id: string;
  created_at: string;
  confidence_state: string;
  crop: string;
  district: string;
}

export default function Dashboard() {
  const [queue, setQueue] = useState<QueueItem[]>([]);
  const [filterState, setFilterState] = useState<string>("ALL");

  useEffect(() => {
    // Mock queue fetch or API call
    setQueue([
      {
        advisory_id: "adv-101",
        created_at: "2026-09-30 12:45",
        confidence_state: "POSSIBLE",
        crop: "rice",
        district: "Palakkad"
      },
      {
        advisory_id: "adv-102",
        created_at: "2026-09-30 11:30",
        confidence_state: "UNCERTAIN",
        crop: "banana",
        district: "Wayanad"
      }
    ]);
  }, []);

  const filtered = queue.filter(
    (item) => filterState === "ALL" || item.confidence_state === filterState
  );

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <header className="flex justify-between items-center pb-6 border-b border-gray-800">
        <h1 className="text-2xl font-bold text-green-400">Expert Review Queue</h1>
        <div className="flex items-center space-x-4">
          <span className="bg-green-900 text-green-300 text-xs px-3 py-1 rounded-full">
            {filtered.length} Pending Reviews
          </span>
          <button
            onClick={() => {
              localStorage.removeItem("expert_token");
              window.location.href = "/login";
            }}
            className="text-xs text-gray-400 hover:text-white"
          >
            Logout
          </button>
        </div>
      </header>

      <div className="my-6 flex gap-4">
        <select
          value={filterState}
          onChange={(e) => setFilterState(e.target.value)}
          className="bg-gray-800 text-white rounded p-2 text-sm border border-gray-700"
        >
          <option value="ALL">All Confidence States</option>
          <option value="POSSIBLE">POSSIBLE</option>
          <option value="UNCERTAIN">UNCERTAIN</option>
          <option value="INSUFFICIENT_DATA">INSUFFICIENT_DATA</option>
        </select>
      </div>

      <div className="overflow-x-auto rounded-lg border border-gray-800 bg-gray-800/50">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-800 text-gray-400 uppercase text-xs">
            <tr>
              <th className="p-4">Created At</th>
              <th className="p-4">Crop</th>
              <th className="p-4">Confidence State</th>
              <th className="p-4">District</th>
              <th className="p-4">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800">
            {filtered.map((row) => (
              <tr key={row.advisory_id} className="hover:bg-gray-800/80">
                <td className="p-4">{row.created_at}</td>
                <td className="p-4 capitalize font-semibold">{row.crop}</td>
                <td className="p-4">
                  <span className="px-2 py-1 rounded text-xs bg-yellow-900/50 text-yellow-300">
                    {row.confidence_state}
                  </span>
                </td>
                <td className="p-4">{row.district}</td>
                <td className="p-4">
                  <Link
                    to={`/review/${row.advisory_id}`}
                    className="bg-green-600 hover:bg-green-500 text-white px-3 py-1 rounded text-xs font-semibold"
                  >
                    Review
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
