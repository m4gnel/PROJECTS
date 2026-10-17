import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, Terminal, Activity } from 'lucide-react';

export function AgentTracePanel({ runs }: { runs: any[] }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!runs || runs.length === 0) return null;

  return (
    <div className="mt-8 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden bg-white dark:bg-slate-900 shadow-sm">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-6 py-4 flex items-center justify-between bg-slate-50 dark:bg-slate-900/80 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
      >
        <div className="flex items-center gap-2 text-slate-900 dark:text-white font-semibold">
          <Activity className="w-5 h-5 text-indigo-500" />
          Agent Trace Logs
        </div>
        {isOpen ? <ChevronUp className="w-5 h-5 text-slate-500" /> : <ChevronDown className="w-5 h-5 text-slate-500" />}
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-t border-slate-200 dark:border-slate-800"
          >
            <div className="p-4 bg-slate-950 text-slate-300 font-mono text-sm max-h-96 overflow-y-auto">
              {runs.map((run, i) => (
                <div key={i} className="mb-4 last:mb-0">
                  <div className="flex items-center gap-2 text-indigo-400 mb-1">
                    <Terminal className="w-4 h-4" />
                    <span className="uppercase font-bold tracking-wider">{run.agent_role}</span>
                    <span className="text-slate-500">|</span>
                    <span className={run.status === 'done' ? 'text-emerald-400' : run.status === 'failed' ? 'text-rose-400' : 'text-amber-400'}>
                      [{run.status}]
                    </span>
                  </div>
                  {run.raw_output && (
                    <pre className="pl-6 whitespace-pre-wrap break-words text-slate-400 text-xs">
                      {JSON.stringify(run.raw_output, null, 2)}
                    </pre>
                  )}
                  {run.error_detail && (
                    <div className="pl-6 text-rose-400 text-xs mt-1">
                      ERROR: {run.error_detail}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
