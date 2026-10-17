import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertTriangle, XCircle, Info } from 'lucide-react';

interface Claim {
  id: string;
  claim_text: string;
  verification_status: string;
  supporting_source_ids: string[];
  conflicting_source_ids: string[];
}

export function FactCheckTable({ claims }: { claims: Claim[] }) {
  if (!claims || claims.length === 0) return null;

  const getStatusConfig = (status: string) => {
    switch (status) {
      case 'verified':
        return { icon: <CheckCircle className="w-5 h-5 text-emerald-500" />, bg: 'bg-emerald-500/10', text: 'text-emerald-700 dark:text-emerald-400' };
      case 'partially_verified':
        return { icon: <Info className="w-5 h-5 text-amber-500" />, bg: 'bg-amber-500/10', text: 'text-amber-700 dark:text-amber-400' };
      case 'contradicted':
        return { icon: <AlertTriangle className="w-5 h-5 text-rose-500" />, bg: 'bg-rose-500/10', text: 'text-rose-700 dark:text-rose-400' };
      case 'unverified':
      default:
        return { icon: <XCircle className="w-5 h-5 text-slate-400" />, bg: 'bg-slate-500/10', text: 'text-slate-600 dark:text-slate-400' };
    }
  };

  return (
    <div className="my-8 rounded-xl border border-slate-200 dark:border-slate-800 overflow-hidden bg-white dark:bg-slate-900 shadow-sm">
      <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-indigo-500" />
          Fact-Check Analysis
        </h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-slate-500 uppercase bg-slate-50/50 dark:bg-slate-900/50 dark:text-slate-400">
            <tr>
              <th className="px-6 py-4 font-medium">Claim</th>
              <th className="px-6 py-4 font-medium">Status</th>
              <th className="px-6 py-4 font-medium">Sources (Support / Conflict)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
            {claims.map((claim, idx) => {
              const config = getStatusConfig(claim.verification_status);
              return (
                <motion.tr 
                  key={idx}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
                >
                  <td className="px-6 py-4 font-medium text-slate-900 dark:text-slate-200 w-1/2">
                    {claim.claim_text}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${config.bg} ${config.text}`}>
                      {config.icon}
                      {claim.verification_status.replace('_', ' ').toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-500 dark:text-slate-400">
                    <div className="flex gap-4">
                      <span className="text-emerald-600 dark:text-emerald-400 font-medium">
                        {claim.supporting_source_ids?.length || 0}
                      </span>
                      <span className="text-rose-600 dark:text-rose-400 font-medium">
                        {claim.conflicting_source_ids?.length || 0}
                      </span>
                    </div>
                  </td>
                </motion.tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
