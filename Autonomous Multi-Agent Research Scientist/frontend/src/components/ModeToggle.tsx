"use client";
import React from 'react';
import { useRouter } from 'next/navigation';
import { MessageSquare, Microscope } from 'lucide-react';

interface ModeToggleProps {
  mode: 'daily' | 'research';
  onChange?: (value: 'daily' | 'research') => void;
}

export function ModeToggle({ mode, onChange }: ModeToggleProps) {
  const router = useRouter();

  const handleSwitch = (nextMode: 'daily' | 'research') => {
    onChange?.(nextMode);
    if (nextMode === 'daily') {
      router.push('/home');
    } else {
      router.push('/research');
    }
  };
  
  return (
    <div className="flex p-1 bg-slate-100 dark:bg-slate-800 rounded-lg w-fit">
      <button
        onClick={() => handleSwitch('daily')}
        className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
          mode === 'daily' 
            ? 'bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-400 shadow-sm' 
            : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'
        }`}
      >
        <MessageSquare className="w-4 h-4" />
        Daily Assistant
      </button>
      <button
        onClick={() => handleSwitch('research')}
        className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
          mode === 'research' 
            ? 'bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-400 shadow-sm' 
            : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'
        }`}
      >
        <Microscope className="w-4 h-4" />
        Deep Research
      </button>
    </div>
  );
}
