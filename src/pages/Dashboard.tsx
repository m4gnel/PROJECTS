import React, { useState, useEffect } from 'react';
import { blink } from '@/lib/blink';
import { useBlinkAuth } from '@blinkdotnew/react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { 
  Plus, 
  Briefcase, 
  Calendar, 
  ChevronRight, 
  History, 
  Award, 
  Clock, 
  LayoutDashboard, 
  TrendingUp, 
  Settings, 
  LogOut,
  Play,
  BrainCircuit
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { format } from 'date-fns';

interface Interview {
  id: string;
  userId: string;
  field: string;
  category: string;
  experienceLevel: string;
  status: 'in_progress' | 'completed';
  score: number | null;
  createdAt: string;
}

export function Dashboard() {
  const { user } = useBlinkAuth();
  const navigate = useNavigate();
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  
  // Form state
  const [field, setField] = useState('');
  const [category, setCategory] = useState('Behavioral');
  const [experienceLevel, setExperienceLevel] = useState('Intermediate');

  useEffect(() => {
    fetchInterviews();
  }, [user]);

  const fetchInterviews = async () => {
    if (!user) return;
    try {
      const data = await blink.db.interviews.list({
        where: { userId: user.id },
        orderBy: { createdAt: 'desc' }
      });
      setInterviews(data as Interview[]);
    } catch (error) {
      console.error('Error fetching interviews:', error);
      toast.error('Failed to load interviews');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartInterview = async () => {
    if (!field) {
      toast.error('Please specify a role or field');
      return;
    }

    setIsCreating(true);
    try {
      const interview = await blink.db.interviews.create({
        userId: user?.id,
        field,
        category,
        experienceLevel,
        status: 'in_progress',
      });
      
      toast.success('Interview session initialized!');
      navigate(`/interview/${interview.id}`);
    } catch (error) {
      console.error('Error starting interview:', error);
      toast.error('Failed to start interview');
    } finally {
      setIsCreating(false);
    }
  };

  const handleLogout = () => {
    blink.auth.signOut();
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Sidebar */}
      <aside className="w-72 border-r border-border flex flex-col glass-dark hidden lg:flex">
        <div className="p-8 border-b border-border flex items-center gap-3">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-lg shadow-primary/20">
            <Briefcase className="text-white w-6 h-6" />
          </div>
          <span className="font-bold text-2xl tracking-tighter">Coach AI</span>
        </div>
        
        <nav className="flex-1 p-6 space-y-2 overflow-y-auto">
          <Button variant="secondary" className="w-full justify-start gap-3 h-12 rounded-xl" size="lg">
            <LayoutDashboard className="w-5 h-5" />
            Dashboard
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-3 h-12 rounded-xl text-muted-foreground hover:text-primary transition-all" size="lg">
            <History className="w-5 h-5" />
            Interview History
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-3 h-12 rounded-xl text-muted-foreground hover:text-primary transition-all" size="lg">
            <TrendingUp className="w-5 h-5" />
            Performance Insights
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-3 h-12 rounded-xl text-muted-foreground hover:text-primary transition-all" size="lg">
            <Settings className="w-5 h-5" />
            Settings
          </Button>
        </nav>

        <div className="p-6 border-t border-border">
          <div className="flex items-center gap-4 mb-6 px-2">
            <div className="relative">
              <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user?.email}`} alt="Avatar" className="w-12 h-12 rounded-full border-2 border-primary/20 bg-muted" />
              <div className="absolute bottom-0 right-0 w-3.5 h-3.5 bg-green-500 border-2 border-card rounded-full shadow-sm" />
            </div>
            <div className="overflow-hidden">
              <p className="font-bold truncate text-sm">{user?.email?.split('@')[0]}</p>
              <p className="text-xs text-muted-foreground flex items-center gap-1">
                <Award className="w-3 h-3 text-primary" />
                Pro Member
              </p>
            </div>
          </div>
          <Button variant="ghost" className="w-full justify-start gap-3 h-12 rounded-xl text-destructive hover:text-destructive hover:bg-destructive/10 transition-all font-bold" onClick={handleLogout}>
            <LogOut className="w-5 h-5" />
            Sign Out
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden relative">
        <header className="h-20 border-b border-border px-8 flex items-center justify-between bg-card/50 backdrop-blur-md sticky top-0 z-20">
          <div>
            <h2 className="text-2xl font-bold tracking-tight">Recruiter Dashboard</h2>
          </div>
          
          <Dialog>
            <DialogTrigger asChild>
              <Button className="gap-2 h-12 px-6 rounded-full shadow-xl shadow-primary/20 transition-all hover:scale-105">
                <Plus className="w-5 h-5" />
                New Simulation
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px] rounded-[2rem] p-8">
              <DialogHeader className="mb-6">
                <DialogTitle className="text-2xl font-bold">Configure Interview</DialogTitle>
                <DialogDescription className="text-lg">
                  Set the parameters for your AI-powered interview session.
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-6 py-4">
                <div className="grid gap-3">
                  <Label htmlFor="field" className="text-base font-bold">Target Role / Industry</Label>
                  <Input 
                    id="field" 
                    placeholder="e.g. Senior Frontend Engineer" 
                    value={field}
                    onChange={(e) => setField(e.target.value)}
                    className="h-12 rounded-xl text-lg px-4"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="grid gap-3">
                    <Label htmlFor="category" className="text-base font-bold">Interview Type</Label>
                    <Select value={category} onValueChange={setCategory}>
                      <SelectTrigger className="h-12 rounded-xl">
                        <SelectValue placeholder="Category" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Behavioral">Behavioral</SelectItem>
                        <SelectItem value="Technical">Technical</SelectItem>
                        <SelectItem value="Case Study">Case Study</SelectItem>
                        <SelectItem value="Cultural Fit">Cultural Fit</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="grid gap-3">
                    <Label htmlFor="level" className="text-base font-bold">Experience Level</Label>
                    <Select value={experienceLevel} onValueChange={setExperienceLevel}>
                      <SelectTrigger className="h-12 rounded-xl">
                        <SelectValue placeholder="Level" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Entry Level">Entry Level</SelectItem>
                        <SelectItem value="Intermediate">Intermediate</SelectItem>
                        <SelectItem value="Senior">Senior</SelectItem>
                        <SelectItem value="Lead/Executive">Lead/Executive</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>
              <DialogFooter className="mt-8 gap-3 sm:flex-row flex-col">
                <Button variant="outline" className="h-12 rounded-xl border-2 flex-1" onClick={() => {}}>Cancel</Button>
                <Button onClick={handleStartInterview} disabled={isCreating} className="h-12 rounded-xl flex-1 shadow-lg shadow-primary/10">
                  {isCreating ? 'Initializing...' : 'Begin Session'}
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </header>

        <div className="flex-1 overflow-y-auto p-8 lg:p-12 space-y-12">
          {/* Stats Bar */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { label: 'Total Simulations', value: interviews.length, icon: BrainCircuit, color: 'bg-blue-500/10 text-blue-500', trend: '+12%' },
              { label: 'Average Performance', value: interviews.length > 0 ? `${Math.round(interviews.reduce((acc, i) => acc + (i.score || 0), 0) / interviews.length)}%` : '--', icon: TrendingUp, color: 'bg-green-500/10 text-green-500', trend: '+5%' },
              { label: 'Hours Practiced', value: '4.5h', icon: Clock, color: 'bg-purple-500/10 text-purple-500', trend: 'Active' },
            ].map((stat, i) => (
              <Card key={i} className="border-border shadow-md hover:shadow-xl transition-all rounded-3xl overflow-hidden group">
                <CardContent className="p-8">
                  <div className="flex items-center justify-between mb-4">
                    <div className={`p-4 rounded-2xl ${stat.color} group-hover:scale-110 transition-transform`}>
                      <stat.icon className="w-8 h-8" />
                    </div>
                    <Badge variant="secondary" className="rounded-full px-3 py-1 font-bold text-xs">{stat.trend}</Badge>
                  </div>
                  <div>
                    <p className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-1">{stat.label}</p>
                    <p className="text-4xl font-black">{stat.value}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Sessions List */}
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-3xl font-black tracking-tighter">Recent Sessions</h3>
              <Button variant="link" className="text-primary font-bold text-lg p-0">View All Archive</Button>
            </div>
            
            {isLoading ? (
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="h-28 w-full bg-muted/30 rounded-[2rem] animate-pulse border border-border" />
                ))}
              </div>
            ) : interviews.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-20 text-center glass rounded-[3rem] border-dashed border-2">
                <div className="w-24 h-24 bg-muted/50 rounded-full flex items-center justify-center mb-6">
                  <History className="w-12 h-12 text-muted-foreground" />
                </div>
                <h3 className="text-2xl font-bold mb-3">No simulation data found</h3>
                <p className="text-muted-foreground text-lg mb-8 max-w-sm">Launch your first realistic AI-driven interview simulation to get performance data.</p>
                <Button size="lg" className="h-14 px-10 rounded-full text-lg font-bold shadow-xl" onClick={() => {}}>Launch First Simulator</Button>
              </div>
            ) : (
              <div className="grid gap-6">
                {interviews.map((interview) => (
                  <div 
                    key={interview.id} 
                    className="group glass p-8 rounded-[2rem] flex items-center justify-between hover:border-primary/40 transition-all cursor-pointer shadow-sm hover:shadow-2xl animate-reveal"
                    onClick={() => navigate(interview.status === 'completed' ? `/feedback/${interview.id}` : `/interview/${interview.id}`)}
                  >
                    <div className="flex items-center gap-8">
                      <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center group-hover:scale-110 group-hover:bg-primary group-hover:text-white transition-all shadow-inner">
                        <Award className="w-8 h-8" />
                      </div>
                      <div>
                        <div className="flex items-center gap-4 mb-2">
                          <h4 className="font-black text-2xl tracking-tight">{interview.field}</h4>
                          <Badge variant="secondary" className="rounded-full px-4 py-1 text-xs font-bold uppercase tracking-widest glass border-primary/10">{interview.category}</Badge>
                        </div>
                        <div className="flex items-center gap-6 text-base text-muted-foreground font-medium">
                          <span className="flex items-center gap-2"><Calendar className="w-4 h-4 text-primary" /> {format(new Date(interview.createdAt), 'MMM d, yyyy')}</span>
                          <span className="flex items-center gap-2 underline decoration-primary/30 decoration-2 underline-offset-4">{interview.experienceLevel}</span>
                          <Badge variant={interview.status === 'completed' ? 'default' : 'outline'} className="rounded-full px-3">
                            {interview.status === 'completed' ? 'Fully Analyzed' : 'In Progress'}
                          </Badge>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-12">
                      <div className="text-right">
                        <p className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-1">Impact Score</p>
                        <p className={`text-4xl font-black ${interview.score && interview.score > 80 ? 'text-primary' : 'text-foreground'}`}>
                          {interview.score ? `${interview.score}%` : '--'}
                        </p>
                      </div>
                      <div className="w-14 h-14 rounded-full flex items-center justify-center border-2 border-border group-hover:border-primary group-hover:bg-primary group-hover:text-white transition-all">
                        <ChevronRight className="w-6 h-6" />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Upsell / Info */}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 pb-12">
            <Card className="bg-primary text-primary-foreground border-none rounded-[3rem] shadow-2xl overflow-hidden group">
              <CardContent className="p-10 relative h-full flex flex-col">
                <div className="relative z-10">
                  <Badge variant="outline" className="mb-6 text-white border-white/30 px-4 py-1 rounded-full text-xs font-bold">NEW FEATURE</Badge>
                  <h3 className="text-4xl font-black tracking-tighter mb-4">Elite Simulation Mode</h3>
                  <p className="text-primary-foreground/80 text-xl mb-10 max-w-sm leading-relaxed font-medium">
                    Face our most aggressive AI recruiters designed to simulate high-stakes Silicon Valley interviews.
                  </p>
                  <Button variant="secondary" className="h-14 px-8 text-lg font-black rounded-2xl mt-auto shadow-xl group-hover:scale-105 transition-transform">
                    Unlock Elite Mode
                  </Button>
                </div>
                <div className="absolute -bottom-12 -right-12 p-8 opacity-20 group-hover:rotate-12 group-hover:scale-110 transition-all duration-700">
                  <Play className="w-64 h-64 fill-white" />
                </div>
              </CardContent>
            </Card>

            <Card className="glass border-primary/10 rounded-[3rem] shadow-xl overflow-hidden group">
              <CardContent className="p-10 relative h-full flex flex-col">
                <div className="relative z-10">
                  <Badge variant="outline" className="mb-6 border-primary/30 px-4 py-1 rounded-full text-xs font-bold">ANALYTICS</Badge>
                  <h3 className="text-4xl font-black tracking-tighter mb-4 text-foreground">Gap Analysis</h3>
                  <p className="text-muted-foreground text-xl mb-10 max-w-sm leading-relaxed font-medium">
                    Discover exactly where your storytelling fails and get concrete actions to improve your STAR stories.
                  </p>
                  <Button variant="outline" className="h-14 px-8 text-lg font-black rounded-2xl mt-auto border-2 transition-all hover:bg-primary/5">
                    Run Analysis Report
                  </Button>
                </div>
                <div className="absolute -bottom-12 -right-12 p-8 opacity-5 text-primary group-hover:-rotate-12 group-hover:scale-110 transition-all duration-700">
                  <TrendingUp className="w-64 h-64" />
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Decorative background glow */}
        <div className="absolute -top-32 -right-32 w-96 h-96 bg-primary/5 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute -bottom-32 -left-32 w-96 h-96 bg-accent/5 rounded-full blur-[100px] pointer-events-none" />
      </main>
    </div>
  );
}
