import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { blink } from '@/lib/blink';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Award, 
  ChevronLeft, 
  Download, 
  Share2, 
  CheckCircle2, 
  Target, 
  Zap, 
  BarChart3,
  TrendingUp,
  BrainCircuit,
  Loader2,
  Trophy,
  ArrowRight
} from 'lucide-react';
import { toast } from 'react-hot-toast';

interface Interview {
  id: string;
  field: string;
  category: string;
  experienceLevel: string;
  score: number;
  overallFeedback: string;
  createdAt: string;
}

export function FeedbackView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [interview, setInterview] = useState<Interview | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchResult() {
      if (!id) return;
      try {
        const data = await blink.db.interviews.get(id) as Interview;
        if (!data) {
          toast.error('Session results not found');
          navigate('/dashboard');
          return;
        }
        setInterview(data);
      } catch (error) {
        console.error('Failed to fetch results:', error);
        toast.error('Error loading feedback');
      } finally {
        setIsLoading(false);
      }
    }
    fetchResult();
  }, [id]);

  if (isLoading || !interview) {
    return (
      <div className="h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-primary animate-spin mx-auto mb-4" />
          <p className="text-xl font-bold">Analyzing Performance Data...</p>
        </div>
      </div>
    );
  }

  const metrics = [
    { label: 'Communication', score: interview.score - 5, desc: 'Clarity, tone, and pacing of your responses.' },
    { label: 'Technical Depth', score: interview.score + 2, desc: 'Domain expertise and concept understanding.' },
    { label: 'STAR Structure', score: interview.score - 10, desc: 'Adherence to the Situation-Task-Action-Result framework.' },
    { label: 'Confidence', score: interview.score + 5, desc: 'Response resilience and poise under pressure.' },
  ];

  return (
    <div className="min-h-screen bg-background">
      <header className="h-20 border-b border-border px-8 flex items-center justify-between bg-card/50 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-6">
          <Button variant="ghost" className="rounded-full gap-2 font-bold" onClick={() => navigate('/dashboard')}>
            <ChevronLeft className="w-5 h-5" />
            Exit Report
          </Button>
          <div className="h-8 w-px bg-border hidden md:block" />
          <div className="hidden md:block">
            <h2 className="text-xl font-black tracking-tight">{interview.field} Report</h2>
            <p className="text-sm text-muted-foreground font-medium">{interview.category} · {interview.experienceLevel}</p>
          </div>
        </div>
        <div className="flex gap-4">
          <Button variant="outline" className="rounded-full gap-2 border-2 h-11 hidden sm:flex">
            <Share2 className="w-4 h-4" />
            Share Report
          </Button>
          <Button className="rounded-full gap-2 shadow-lg h-11 shadow-primary/20">
            <Download className="w-4 h-4" />
            Export PDF
          </Button>
        </div>
      </header>

      <main className="container max-w-6xl mx-auto py-12 px-6 space-y-12">
        {/* Score Hero */}
        <section className="animate-reveal">
          <Card className="rounded-[3rem] overflow-hidden border-none bg-primary text-primary-foreground shadow-3xl relative">
            <CardContent className="p-12 md:p-20 flex flex-col md:flex-row items-center gap-12 relative z-10">
              <div className="relative">
                <div className="w-56 h-56 md:w-64 md:h-64 rounded-full border-[12px] border-white/20 flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-7xl md:text-8xl font-black">{interview.score}%</p>
                    <p className="text-lg font-bold opacity-80 uppercase tracking-widest mt-1">Impact Score</p>
                  </div>
                </div>
                <div className="absolute -top-4 -right-4 w-20 h-20 bg-accent rounded-full flex items-center justify-center shadow-2xl animate-float">
                  <Trophy className="w-10 h-10 text-primary-foreground" />
                </div>
              </div>
              <div className="flex-1 space-y-6">
                <Badge variant="secondary" className="bg-white/20 text-white border-none rounded-full px-6 py-1.5 text-base font-black tracking-tight">
                  IMPRESSIVE PERFORMANCE
                </Badge>
                <h1 className="text-4xl md:text-6xl font-black tracking-tighter leading-tight">
                  You're in the top 15% <br /> for this position.
                </h1>
                <p className="text-xl font-medium opacity-90 leading-relaxed max-w-xl">
                  Your communication skills are strong, but there is room for improvement in your STAR structure alignment. 
                  Focus on specific outcomes in your behavioral answers.
                </p>
                <div className="flex gap-4 pt-4">
                  <div className="flex items-center gap-2 font-bold bg-white/10 px-4 py-2 rounded-2xl">
                    <CheckCircle2 className="w-5 h-5 text-accent" /> High Confidence
                  </div>
                  <div className="flex items-center gap-2 font-bold bg-white/10 px-4 py-2 rounded-2xl">
                    <Target className="w-5 h-5 text-accent" /> Strong Technical Depth
                  </div>
                </div>
              </div>
            </CardContent>
            {/* Background Decoration */}
            <div className="absolute top-0 right-0 p-12 opacity-10">
              <TrendingUp className="w-96 h-96" />
            </div>
          </Card>
        </section>

        {/* Detailed Breakdown */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-12 animate-reveal [animation-delay:200ms]">
          <div className="space-y-8">
            <h3 className="text-4xl font-black tracking-tighter">Skill Analysis</h3>
            <div className="grid gap-6">
              {metrics.map((m, i) => (
                <div key={i} className="glass p-8 rounded-[2rem] space-y-4 shadow-sm hover:shadow-xl transition-all border-transparent hover:border-primary/20 group">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="text-2xl font-black tracking-tight">{m.label}</h4>
                    <p className="text-3xl font-black text-primary">{m.score}%</p>
                  </div>
                  <Progress value={m.score} className="h-4 rounded-full bg-secondary" />
                  <p className="text-muted-foreground font-medium text-lg leading-relaxed">{m.desc}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-8">
            <h3 className="text-4xl font-black tracking-tighter">Coach's Remarks</h3>
            <div className="glass p-10 rounded-[2rem] relative overflow-hidden h-full">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-14 h-14 bg-primary rounded-2xl flex items-center justify-center shadow-lg shadow-primary/20">
                  <BrainCircuit className="text-white w-8 h-8" />
                </div>
                <div>
                  <p className="font-black text-xl leading-none">Alex's Final Analysis</p>
                  <p className="text-muted-foreground font-bold uppercase tracking-widest text-xs mt-1">Lead Recruiter AI</p>
                </div>
              </div>
              <div className="prose prose-lg dark:prose-invert max-w-none">
                <p className="text-xl leading-relaxed text-foreground/90 italic font-medium">
                  {interview.overallFeedback || "You displayed a high degree of domain expertise throughout the session. Your explanation of complex systems was clear and concise. To reach the executive level, I recommend working on your 'Situation' context setting—keep it under 45 seconds to leave more time for your specific 'Actions'."}
                </p>
              </div>
              <div className="mt-12 space-y-4 pt-8 border-t border-border">
                <p className="font-black text-xs uppercase tracking-widest text-muted-foreground">Recommended Training</p>
                <div className="flex flex-wrap gap-3">
                  <Badge variant="outline" className="rounded-full px-4 py-2 border-2 font-bold hover:bg-primary hover:text-white transition-all cursor-pointer">Behavioral Storytelling</Badge>
                  <Badge variant="outline" className="rounded-full px-4 py-2 border-2 font-bold hover:bg-primary hover:text-white transition-all cursor-pointer">Impact Scaling</Badge>
                  <Badge variant="outline" className="rounded-full px-4 py-2 border-2 font-bold hover:bg-primary hover:text-white transition-all cursor-pointer">Executive Presence</Badge>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Question Log */}
        <section className="space-y-8 pb-20 animate-reveal [animation-delay:400ms]">
          <h3 className="text-4xl font-black tracking-tighter">Question-by-Question Review</h3>
          <div className="grid gap-6">
            {[1, 2, 3].map((q) => (
              <Card key={q} className="rounded-[2.5rem] border-2 border-border shadow-md hover:border-primary/20 transition-all overflow-hidden group">
                <CardHeader className="p-8 md:p-10 border-b border-border bg-card/30">
                  <div className="flex justify-between items-start gap-4">
                    <div className="flex gap-6">
                      <div className="w-12 h-12 rounded-2xl bg-secondary flex items-center justify-center font-black text-xl group-hover:scale-110 transition-transform">
                        {q}
                      </div>
                      <div className="space-y-2">
                        <Badge variant="secondary" className="rounded-full px-3 py-1 font-black text-[10px] uppercase tracking-widest border-primary/10">STRENGTH</Badge>
                        <CardTitle className="text-2xl font-black tracking-tight leading-snug">
                          {q === 1 ? "Tell me about a time you had to handle a major conflict within your team." : 
                           q === 2 ? "How do you stay up-to-date with current industry trends and technologies?" :
                           "What is the most complex project you've led, and what was your specific impact?"}
                        </CardTitle>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-xs font-black text-muted-foreground uppercase tracking-widest mb-1">Score</p>
                      <p className="text-3xl font-black text-primary">92</p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="p-8 md:p-10 bg-background">
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                    <div className="space-y-4">
                      <p className="text-xs font-black text-muted-foreground uppercase tracking-widest">Your Response Transcript</p>
                      <p className="text-lg leading-relaxed text-muted-foreground font-medium">
                        "In my previous role at X, we faced a situation where the design and engineering teams were misaligned on the roadmap. I initiated a series of workshops to..."
                      </p>
                    </div>
                    <div className="bg-primary/5 rounded-[2rem] p-8 border border-primary/10">
                      <p className="text-xs font-black text-primary uppercase tracking-widest mb-4 flex items-center gap-2">
                        <Zap className="w-4 h-4 fill-primary" /> AI Coaching Tip
                      </p>
                      <p className="text-lg leading-relaxed font-bold">
                        Excellent use of the STAR method. You clearly identified your individual contribution. To improve, mention the specific metrics that improved after your intervention.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Footer CTA */}
        <section className="bg-card border-2 border-border rounded-[3rem] p-12 text-center animate-reveal [animation-delay:600ms]">
          <h2 className="text-3xl md:text-4xl font-black tracking-tighter mb-4">Feeling more confident?</h2>
          <p className="text-lg text-muted-foreground mb-8 max-w-xl mx-auto">
            Consistency is key to mastering interviews. Schedule another simulation to practice your improvements.
          </p>
          <Button size="lg" className="h-14 px-10 rounded-full text-lg font-black shadow-xl hover:scale-105 transition-transform" onClick={() => navigate('/interview-session')}>
            Try Another Simulation <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
        </section>
      </main>
    </div>
  );
}
