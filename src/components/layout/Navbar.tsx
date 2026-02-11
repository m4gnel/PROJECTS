import React from 'react';
import { Button } from '@/components/ui/button';
import { useBlinkAuth } from '@blinkdotnew/react';
import { blink } from '@/lib/blink';
import { Briefcase, LayoutDashboard, User, LogOut, MessageSquare } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function Navbar() {
  const { isAuthenticated, user } = useBlinkAuth();
  const navigate = useNavigate();

  const handleLogin = () => {
    blink.auth.login(window.location.origin + '/dashboard');
  };

  const handleLogout = () => {
    blink.auth.signOut();
  };

  return (
    <nav className="h-20 border-b border-border fixed top-0 w-full z-50 glass shadow-sm">
      <div className="container h-full mx-auto px-6 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-lg shadow-primary/20">
            <Briefcase className="text-white w-6 h-6" />
          </div>
          <span className="font-black text-2xl tracking-tighter">Coach AI</span>
        </Link>

        <div className="hidden md:flex items-center gap-10 font-bold text-base text-muted-foreground">
          <Link to="/" className="hover:text-primary transition-colors">How it works</Link>
          <Link to="/" className="hover:text-primary transition-colors">Pricing</Link>
          <Link to="/" className="hover:text-primary transition-colors">Success Stories</Link>
        </div>

        <div className="flex items-center gap-4">
          {!isAuthenticated ? (
            <>
              <Button variant="ghost" className="font-bold text-base" onClick={handleLogin}>Log In</Button>
              <Button className="h-11 px-8 rounded-full font-bold shadow-lg shadow-primary/10" onClick={handleLogin}>
                Sign Up Free
              </Button>
            </>
          ) : (
            <div className="flex items-center gap-4">
              <Button variant="ghost" className="hidden sm:flex font-bold gap-2 rounded-xl" onClick={() => navigate('/dashboard')}>
                <LayoutDashboard className="w-4 h-4" />
                Dashboard
              </Button>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-11 w-11 rounded-full p-0 overflow-hidden border-2 border-primary/20 hover:border-primary transition-all">
                    <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user?.email}`} alt="Avatar" className="w-full h-full object-cover" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56 mt-2 rounded-2xl p-2 shadow-2xl glass" align="end">
                  <DropdownMenuLabel className="font-black px-3 py-2 text-sm truncate">{user?.email}</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem className="rounded-xl h-10 font-medium" onClick={() => navigate('/dashboard')}>
                    <LayoutDashboard className="mr-2 h-4 w-4" />
                    Dashboard
                  </DropdownMenuItem>
                  <DropdownMenuItem className="rounded-xl h-10 font-medium">
                    <User className="mr-2 h-4 w-4" />
                    Profile Settings
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem className="rounded-xl h-10 font-bold text-destructive focus:text-destructive focus:bg-destructive/10" onClick={handleLogout}>
                    <LogOut className="mr-2 h-4 w-4" />
                    Sign Out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
