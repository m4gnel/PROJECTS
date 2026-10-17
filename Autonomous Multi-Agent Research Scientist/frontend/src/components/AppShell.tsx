'use client';

import Link from 'next/link';
import type { ReactNode } from 'react';
import { BookOpen, Compass, Home, Library, Search, Settings, Sparkles, UserRound } from 'lucide-react';

const navItems = [
  { label: 'Home', href: '/home', icon: Home },
  { label: 'Search', href: '/research', icon: Search },
  { label: 'Library', href: '#', icon: Library },
  { label: 'Spaces', href: '#', icon: BookOpen },
  { label: 'Settings', href: '#', icon: Settings },
];

interface AppShellProps {
  children: ReactNode;
  activeItem?: 'home' | 'search' | 'library' | 'spaces' | 'settings';
  title?: string;
  subtitle?: string;
}

export function AppShell({ children, activeItem = 'home', title, subtitle }: AppShellProps) {
  return (
    <div className="min-h-screen bg-[#171615] text-[#f2e9dc]">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col lg:flex-row">
        <aside className="border-b border-[#2d2925] bg-[#151312]/95 px-4 py-4 lg:sticky lg:top-0 lg:min-h-screen lg:w-64 lg:border-b-0 lg:border-r lg:px-5 lg:py-6">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl border border-[#3e3730] bg-[#1f1b18] text-[#5d9ea4]">
              <Compass className="h-5 w-5" />
            </div>
            <div>
              <p className="text-[12px] uppercase tracking-[0.3em] text-[#8f857c]">answer engine</p>
              <p className="text-[16px] font-medium text-[#f3eadf]">perplexity</p>
            </div>
          </div>

          <nav className="mt-8 flex flex-col gap-1">
            {navItems.map(({ label, href, icon: Icon }) => {
              const isActive =
                label.toLowerCase() === activeItem ||
                (label === 'Home' && activeItem === 'home') ||
                (label === 'Search' && activeItem === 'search');

              return (
                <Link
                  key={label}
                  href={href}
                  className={`flex items-center gap-3 rounded-2xl px-3 py-2.5 text-sm transition-colors ${
                    isActive
                      ? 'bg-[#1f1b18] text-[#5d9ea4] shadow-[inset_0_0_0_1px_rgba(93,158,164,0.18)]'
                      : 'text-[#a79d90] hover:bg-[#201c18] hover:text-[#efe5d7]'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{label}</span>
                </Link>
              );
            })}
          </nav>

          <div className="mt-8 rounded-[20px] border border-[#2e2924] bg-[#1b1816] p-3">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#1f1b18] text-[#5d9ea4]">
                <UserRound className="h-4 w-4" />
              </div>
              <div>
                <p className="text-[13px] font-medium text-[#f3eadf]">Signed in</p>
                <p className="text-[12px] text-[#8f857c]">Research workspace</p>
              </div>
            </div>
          </div>
        </aside>

        <div className="flex-1">
          <header className="border-b border-[#2d2925] px-4 py-3 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between gap-3">
              <div className="min-w-0">
                {title ? <p className="text-[13px] font-medium text-[#f3eadf]">{title}</p> : null}
                {subtitle ? <p className="truncate text-[12px] text-[#8f857c]">{subtitle}</p> : null}
              </div>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  className="rounded-full border border-[#3a342f] bg-[#1d1a17] px-3 py-1.5 text-[12px] text-[#bdb1a4] transition-colors hover:border-[#5d9ea4] hover:text-[#f3eadf]"
                >
                  New search
                </button>
                <button
                  type="button"
                  className="rounded-full border border-[#3a342f] bg-[#1d1a17] px-3 py-1.5 text-[12px] text-[#bdb1a4] transition-colors hover:border-[#5d9ea4] hover:text-[#f3eadf]"
                >
                  Share
                </button>
                <div className="flex h-9 w-9 items-center justify-center rounded-full border border-[#3a342f] bg-[#1d1a17] text-[#5d9ea4]">
                  <Sparkles className="h-4 w-4" />
                </div>
              </div>
            </div>
          </header>

          <main className="px-4 py-6 sm:px-6 lg:px-8 lg:py-8">{children}</main>
        </div>
      </div>
    </div>
  );
}
