"use client";

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { AppShell } from '@/components/AppShell';
import { ArrowUpRight, Loader2, Send, Sparkles } from 'lucide-react';

const quickPrompts = ["Market trends in AI infrastructure", "Best sources for startup validation", "Summarize this research brief"];

export default function HomePage() {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([
    {
      role: 'assistant',
      content: 'I can help you move from a rough question to a precise research answer. Start with a topic and I’ll structure the best next steps.',
    },
  ]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input;
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/v1/chat/daily', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg }),
      });

      const data = await res.json();
      setMessages((prev) => [...prev, { role: 'assistant', content: data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'assistant', content: 'The backend is unavailable right now. Please try again in a moment.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppShell activeItem="home" title="AMRS research workspace" subtitle="Ask, verify, and refine in one calm workspace">
      <div className="mx-auto flex max-w-3xl flex-col">
        <div className="mb-8 flex flex-col items-center text-center">
          <div className="mb-4 flex items-center gap-2 rounded-full border border-[#3a342f] bg-[#1c1917] px-3 py-1.5 text-[12px] text-[#bdb1a4]">
            <Sparkles className="h-3.5 w-3.5 text-[#5d9ea4]" />
            Trusted research answers, grounded and readable
          </div>
          <h1 className="text-[2rem] font-semibold tracking-[-0.03em] text-[#f3eadf] sm:text-[2.6rem]">
            perplexity
          </h1>
          <p className="mt-3 max-w-2xl text-[15px] leading-7 text-[#a79d90]">
            A calm answer engine for research, synthesis, and evidence-forward exploration.
          </p>
        </div>

        <form onSubmit={handleSend} className="rounded-[28px] border border-[#3a342f] bg-[#1c1917] p-3 shadow-[0_10px_40px_rgba(0,0,0,0.2)]">
          <div className="flex items-center gap-3 rounded-[22px] border border-[#332e2a] bg-[#171615] px-4 py-3 focus-within:border-[#5d9ea4] focus-within:shadow-[0_0_0_2px_rgba(93,158,164,0.2)]">
            <Sparkles className="h-5 w-5 shrink-0 text-[#5d9ea4]" />
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything"
              className="flex-1 bg-transparent text-[16px] text-[#f3eadf] outline-none placeholder:text-[#7f766e]"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="flex h-10 w-10 items-center justify-center rounded-full bg-[#5d9ea4] text-[#0f1110] transition-colors hover:bg-[#6ca7ab] disabled:cursor-not-allowed disabled:bg-[#2f2a25] disabled:text-[#6c635a]"
            >
              {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
            </button>
          </div>
          <div className="mt-3 flex flex-wrap items-center gap-2">
            {quickPrompts.map((prompt) => (
              <button
                key={prompt}
                type="button"
                onClick={() => setInput(prompt)}
                className="rounded-full border border-[#342f2a] bg-[#181614] px-3 py-1.5 text-[12px] text-[#bdb1a4] transition-colors hover:border-[#5d9ea4] hover:text-[#f3eadf]"
              >
                {prompt}
              </button>
            ))}
          </div>
        </form>

        <div className="mt-8 space-y-4">
          {messages.slice(1).map((message, index) => (
            <section key={index} className="rounded-[24px] border border-[#322d29] bg-[#191715] p-5 shadow-[0_10px_30px_rgba(0,0,0,0.12)]">
              <div className="mb-3 flex items-center gap-2 text-[12px] uppercase tracking-[0.25em] text-[#7f766e]">
                <span>{message.role === 'user' ? 'You' : 'Answer'}</span>
                <span className="h-1 w-1 rounded-full bg-[#5d9ea4]" />
              </div>
              <div className="prose prose-invert max-w-none text-[15px] leading-7 text-[#d8cdbd] prose-p:my-2 prose-strong:text-[#f3eadf]">
                {message.role === 'user' ? (
                  <p>{message.content}</p>
                ) : (
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                )}
              </div>
              {message.role === 'assistant' ? (
                <div className="mt-4 flex flex-wrap gap-2">
                  {['Sources', 'Follow-up', 'Share'].map((item) => (
                    <button key={item} type="button" className="rounded-full border border-[#342f2a] px-3 py-1.5 text-[12px] text-[#bdb1a4] transition-colors hover:border-[#5d9ea4] hover:text-[#f3eadf]">
                      {item}
                    </button>
                  ))}
                </div>
              ) : null}
            </section>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
