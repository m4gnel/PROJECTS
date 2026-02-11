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
  BrainCircuit,
  PieChart,
  Target
} from 'lucide-react';
import { motion } from 'framer-motion';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip as ChartTooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell
} from 'recharts';
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
  overallFeedback: string | null;
  createdAt: string;
}

export function Dashboard() {
  const { user } = useBlinkAuth();
  const navigate = useNavigate();
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  
  // Mock chart data (in production this would be aggregated from DB)
  const chartData = [
    { name: 'Mon', score: 65 },
    { name: 'Tue', score: 72 },
    { name: 'Wed', score: 68 },
    { name: 'Thu', score: 85 },
    { name: 'Fri', score: 78 },
    { name: 'Sat', score: 92 },
    { name: 'Sun', score: 88 },
  ];

  const categoryData = [
    { name: 'Technical', value: 85, color: '#0D9488' },
    { name: 'Behavioral', value: 72, color: '#2DD4BF' },
    { name: 'Case Study', value: 64, color: '#134E4A' },
    { name: 'Culture', value: 91, color: '#F0FDFA' },
  ];
  
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
    <div className="flex h-screen bg-background overflow-hidden selection:bg-primary selection:text-white">
      {/* Sidebar */}
      <aside className="w-80 border-r border-border flex flex-col glass-dark hidden lg:flex relative z-30">
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] pointer-events-none" />
        
        <div className="p-10 border-b border-border flex items-center gap-3">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-lg shadow-primary/20">
            <Briefcase className="text-white w-6 h-6" />
          </div>
          <span className="font-bold text-2xl tracking-tighter">Coach AI</span>
        </div>
        
        <nav className="flex-1 p-6 space-y-3 overflow-y-auto">
          <Button 
            variant={activeTab === 'overview' ? 'secondary' : 'ghost'} 
            className={`w-full justify-start gap-4 h-14 rounded-2xl text-lg font-bold transition-all ${activeTab === 'overview' ? 'shadow-lg shadow-primary/10' : 'text-muted-foreground hover:text-primary'}`} 
            onClick={() => setActiveTab('overview')}
          >
            <LayoutDashboard className="w-6 h-6" />
            Overview
          </Button>
          <Button 
            variant={activeTab === 'history' ? 'secondary' : 'ghost'} 
            className={`w-full justify-start gap-4 h-14 rounded-2xl text-lg font-bold transition-all ${activeTab === 'history' ? 'shadow-lg shadow-primary/10' : 'text-muted-foreground hover:text-primary'}`}
            onClick={() => setActiveTab('history')}
          >
            <History className="w-6 h-6" />
            History
          </Button>
          <Button 
            variant={activeTab === 'insights' ? 'secondary' : 'ghost'} 
            className={`w-full justify-start gap-4 h-14 rounded-2xl text-lg font-bold transition-all ${activeTab === 'insights' ? 'shadow-lg shadow-primary/10' : 'text-muted-foreground hover:text-primary'}`}
            onClick={() => setActiveTab('insights')}
          >
            <TrendingUp className="w-6 h-6" />
            Insights
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-4 h-14 rounded-2xl text-lg font-bold text-muted-foreground hover:text-primary transition-all" size="lg">
            <Settings className="w-6 h-6" />
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
          <Button variant="ghost" className="w-full justify-start gap-4 h-14 rounded-2xl text-destructive hover:text-destructive hover:bg-destructive/10 transition-all font-bold" onClick={handleLogout}>
            <LogOut className="w-5 h-5" />
            Sign Out
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden relative">
        <header className="h-24 border-b border-border px-10 flex items-center justify-between bg-background/50 backdrop-blur-xl sticky top-0 z-20">
          <div>
            <h2 className="text-3xl font-black tracking-tighter">Command Center</h2>
            <p className="text-muted-foreground font-medium">Welcome back, {user?.email?.split('@')[0]}</p>
          </div>
          
          <Dialog>
            <DialogTrigger asChild>
              <Button className="gap-2 h-14 px-8 rounded-full text-lg font-bold shadow-xl shadow-primary/20 transition-all hover:scale-105">
                <Plus className="w-6 h-6" />
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
          {activeTab === 'overview' && (
            <>
              {/* Stats Bar */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {[
                  { label: 'Total Simulations', value: interviews.length, icon: BrainCircuit, color: 'bg-blue-500/10 text-blue-500', trend: 'Active' },
                  { label: 'Avg Performance', value: interviews.filter(i => i.score).length > 0 ? `${Math.round(interviews.filter(i => i.score).reduce((acc, i) => acc + (i.score || 0), 0) / interviews.filter(i => i.score).length)}%` : '--', icon: TrendingUp, color: 'bg-green-500/10 text-green-500', trend: 'Growing' },
                  { label: 'Mastery Level', value: interviews.length > 5 ? 'Senior' : 'Intermediate', icon: Award, color: 'bg-purple-500/10 text-purple-500', trend: 'Pro' },
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

              {/* Analytics Section */}
              <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                <Card className="xl:col-span-2 glass border-primary/10 rounded-[3rem] shadow-xl overflow-hidden p-8">
                  <div className="flex items-center justify-between mb-8">
                    <div>
                      <h3 className="text-2xl font-black tracking-tight">Performance Velocity</h3>
                      <p className="text-muted-foreground font-medium">Progress over the last 7 days</p>
                    </div>
                    <Badge variant="secondary" className="px-4 py-1 rounded-full font-bold">+18.4% improvement</Badge>
                  </div>
                  <div className="h-[300px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={chartData}>
                        <defs>
                          <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
                            <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: 'hsl(var(--muted-foreground))', fontWeight: 600 }} dy={10} />
                        <YAxis hide />
                        <ChartTooltip 
                          contentStyle={{ backgroundColor: 'hsl(var(--card))', borderRadius: '1.5rem', border: '1px solid hsl(var(--border))', boxShadow: '0 10px 30px -10px rgba(0,0,0,0.1)' }}
                          itemStyle={{ fontWeight: 800, color: 'hsl(var(--primary))' }}
                        />
                        <Area type="monotone" dataKey="score" stroke="hsl(var(--primary))" strokeWidth={4} fillOpacity={1} fill="url(#colorScore)" />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </Card>

                <Card className="glass border-primary/10 rounded-[3rem] shadow-xl overflow-hidden p-8">
                  <div className="mb-8">
                    <h3 className="text-2xl font-black tracking-tight">Skill Breakdown</h3>
                    <p className="text-muted-foreground font-medium">Accuracy by category</p>
                  </div>
                  <div className="space-y-6">
                    {categoryData.map((cat, i) => (
                      <div key={i} className="space-y-2">
                        <div className="flex justify-between items-end">
                          <p className="font-bold text-sm tracking-wide uppercase opacity-70">{cat.name}</p>
                          <p className="font-black text-xl">{cat.value}%</p>
                        </div>
                        <div className="h-3 w-full bg-muted/50 rounded-full overflow-hidden">
                          <motion.div 
                            initial={{ width: 0 }}
                            animate={{ width: `${cat.value}%` }}
                            transition={{ duration: 1, delay: i * 0.1 }}
                            className="h-full bg-primary rounded-full"
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="mt-10 p-6 bg-primary/5 rounded-2xl border border-primary/10 flex items-center gap-4">
                    <Target className="w-10 h-10 text-primary" />
                    <div>
                      <p className="font-black text-sm uppercase tracking-widest text-primary">Primary Focus</p>
                      <p className="font-bold text-foreground">Improve STAR clarity</p>
                    </div>
                  </div>
                </Card>
              </div>
            </>
          )}

          {activeTab === 'history' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-3xl font-black tracking-tighter">Interview Archive</h3>
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
                    <motion.div 
                      key={interview.id} 
                      className="group glass p-8 rounded-[2.5rem] flex items-center justify-between hover:border-primary/40 transition-all cursor-pointer shadow-elegant hover:shadow-glow animate-reveal"
                      onClick={() => navigate(interview.status === 'completed' ? `/feedback/${interview.id}` : `/interview/${interview.id}`)}
                      whileHover={{ scale: 1.02 }}
                      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                    >
                      <div className="flex items-center gap-8">
                        <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center group-hover:scale-110 group-hover:bg-primary group-hover:text-white transition-all">
                          <Award className="w-8 h-8" />
                        </div>
                        <div>
                          <div className="flex items-center gap-4 mb-2">
                            <h4 className="font-black text-2xl tracking-tight leading-none">{interview.field}</h4>
                            <Badge variant="secondary" className="rounded-full px-4 py-1 text-[10px] font-black uppercase tracking-widest glass border-primary/10">{interview.category}</Badge>
                          </div>
                          <div className="flex items-center gap-6 text-sm text-muted-foreground font-bold">
                            <span className="flex items-center gap-2 uppercase tracking-wider"><Calendar className="w-4 h-4 text-primary" /> {format(new Date(interview.createdAt), 'MMM d, yyyy')}</span>
                            <span className="flex items-center gap-2 uppercase tracking-wider underline decoration-primary/30 decoration-2 underline-offset-4">{interview.experienceLevel}</span>
                            <Badge variant={interview.status === 'completed' ? 'default' : 'outline'} className="rounded-full px-3 py-0 h-6 font-black text-[10px] uppercase tracking-tighter">
                              {interview.status === 'completed' ? 'Analyzed' : 'Live Session'}
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
                    </motion.div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'insights' && (
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
          )}
        </div>

        {/* Decorative background glow */}
        <div className="absolute -top-32 -right-32 w-96 h-96 bg-primary/5 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute -bottom-32 -left-32 w-96 h-96 bg-accent/5 rounded-full blur-[100px] pointer-events-none" />
      </main>
    </div>
  );
}
