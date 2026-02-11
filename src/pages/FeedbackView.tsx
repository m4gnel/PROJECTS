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
import { motion } from 'framer-motion';

interface Metric {
  id: string;
  metricName: string;
  score: number;
}

interface Feedback {
  id: string;
  overallScore: number;
  generalFeedback: string;
  strengths: string; // JSON string
  improvements: string; // JSON string
}

interface Interview {
  id: string;
  field: string;
  category: string;
  experienceLevel: string;
  score: number;
  overallFeedback: string;
  analysisData: string;
  createdAt: string;
}

interface Question {
  id: string;
  questionText: string;
  userAnswer: string;
  aiFeedback: string;
  score: number;
}

export function FeedbackView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [interview, setInterview] = useState<Interview | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
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

        // Fetch questions
        const questionsData = await blink.db.questions.list({
          where: { interviewId: id },
          orderBy: { orderIndex: 'asc' }
        });
        setQuestions(questionsData as Question[]);

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

  const analysis = interview.analysisData ? JSON.parse(interview.analysisData) : null;

  const metrics = analysis?.metrics || [
    { name: 'Communication', score: interview.score - 5, description: 'Clarity, tone, and pacing of your responses.' },
    { name: 'Technical Depth', score: interview.score + 2, description: 'Domain expertise and concept understanding.' },
    { name: 'STAR Structure', score: interview.score - 10, description: 'Adherence to the Situation-Task-Action-Result framework.' },
    { name: 'Confidence', score: interview.score + 5, description: 'Response resilience and poise under pressure.' },
  ];

  return (
    <div className="min-h-screen bg-background selection:bg-primary selection:text-white">
      <header className="h-24 border-b border-border px-10 flex items-center justify-between bg-background/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="flex items-center gap-6">
          <Button variant="ghost" className="rounded-full gap-2 font-bold" onClick={() => navigate('/dashboard')}>
            <ChevronLeft className="w-5 h-5" />
            Exit Report
          </Button>
          <div className="h-10 w-px bg-border hidden md:block" />
          <div className="hidden md:block">
            <h2 className="text-2xl font-black tracking-tight">{interview.field} Report</h2>
            <p className="text-sm text-muted-foreground font-medium">{interview.category} · {interview.experienceLevel}</p>
          </div>
        </div>
        <div className="flex gap-4">
          <Button variant="outline" className="rounded-full gap-2 border-2 h-12 hidden sm:flex">
            <Share2 className="w-4 h-4" />
            Share Report
          </Button>
          <Button className="rounded-full gap-2 shadow-lg h-12 shadow-primary/20">
            <Download className="w-4 h-4" />
            Export PDF
          </Button>
        </div>
      </header>

      <main className="container max-w-7xl mx-auto py-16 px-8 space-y-20">
        {/* Score Hero */}
        <section className="animate-reveal">
          <Card className="rounded-[3rem] overflow-hidden border-none bg-primary text-primary-foreground shadow-3xl relative">
            <CardContent className="p-12 md:p-20 flex flex-col md:flex-row items-center gap-12 relative z-10">
              <div className="relative">
                <div className="w-56 h-56 md:w-72 md:h-72 rounded-full border-[16px] border-white/10 flex items-center justify-center shadow-2xl bg-primary/20 backdrop-blur-lg">
                  <div className="text-center">
                    <p className="text-8xl md:text-9xl font-black tracking-tighter">{interview.score}%</p>
                    <p className="text-xl font-black opacity-60 uppercase tracking-widest mt-1">Impact Score</p>
                  </div>
                </div>
                <motion.div 
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute -top-4 -right-4 w-24 h-24 bg-accent rounded-full flex items-center justify-center shadow-2xl"
                >
                  <Trophy className="w-12 h-12 text-primary-foreground" />
                </motion.div>
              </div>
              <div className="flex-1 space-y-8">
                <div className="flex flex-wrap gap-3">
                  <Badge variant="secondary" className="bg-white/10 text-white border-none rounded-full px-6 py-2 text-sm font-black tracking-widest uppercase">
                    {interview.score > 80 ? 'ELITE PERFORMANCE' : 'GROWING STRENGTH'}
                  </Badge>
                  <Badge variant="outline" className="text-white border-white/20 rounded-full px-6 py-2 text-sm font-black tracking-widest uppercase">
                    {interview.field}
                  </Badge>
                </div>
                <h1 className="text-4xl md:text-6xl font-black tracking-tighter leading-tight">
                  {interview.score > 80 ? "You're in the top 15% for this position." : "Solid progress! Let's keep refining your skills."}
                </h1>
                <p className="text-xl font-medium opacity-90 leading-relaxed max-w-xl">
                  {analysis?.coachRemark || interview.overallFeedback || "Your communication skills are strong, but there is room for improvement in your STAR structure alignment."}
                </p>
                <div className="flex flex-wrap gap-4 pt-4">
                  {analysis?.strengths?.slice(0, 2).map((s: string, i: number) => (
                    <div key={i} className="flex items-center gap-2 font-bold bg-white/10 px-4 py-2 rounded-2xl">
                      <CheckCircle2 className="w-5 h-5 text-accent" /> {s}
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
            {/* Background Decoration */}
            <div className="absolute top-0 right-0 p-12 opacity-5">
              <TrendingUp className="w-96 h-96" />
            </div>
          </Card>
        </section>

        {/* Detailed Breakdown */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-12 animate-reveal [animation-delay:200ms]">
          <div className="space-y-8">
            <h3 className="text-4xl font-black tracking-tighter">Skill Analysis</h3>
            <div className="grid gap-6">
              {metrics.map((m: any, i: number) => (
                <div key={i} className="glass p-8 rounded-[2rem] space-y-4 shadow-sm hover:shadow-xl transition-all border-transparent hover:border-primary/20 group">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="text-2xl font-black tracking-tight">{m.name || m.label}</h4>
                    <p className="text-3xl font-black text-primary">{m.score}%</p>
                  </div>
                  <Progress value={m.score} className="h-4 rounded-full bg-secondary" />
                  <p className="text-muted-foreground font-medium text-lg leading-relaxed">{m.description || m.desc}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-8">
            <h3 className="text-4xl font-black tracking-tighter">Strategic Insights</h3>
            <div className="glass p-10 rounded-[2rem] relative overflow-hidden h-full flex flex-col">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-14 h-14 bg-primary rounded-2xl flex items-center justify-center shadow-lg shadow-primary/20">
                  <BrainCircuit className="text-white w-8 h-8" />
                </div>
                <div>
                  <p className="font-black text-xl leading-none">Alex's Final Analysis</p>
                  <p className="text-muted-foreground font-bold uppercase tracking-widest text-xs mt-1">Lead Recruiter AI</p>
                </div>
              </div>
              <div className="space-y-6 flex-1">
                <div className="space-y-2">
                  <p className="font-black text-xs uppercase tracking-widest text-primary">Key Improvements</p>
                  <ul className="space-y-3">
                    {(analysis?.improvements || ["Focus on specific outcomes", "Reduce filler words"]).map((item: string, i: number) => (
                      <li key={i} className="flex gap-3 text-lg font-medium leading-tight">
                        <Zap className="w-5 h-5 text-accent flex-shrink-0" />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="pt-6 border-t border-border">
                   <p className="text-xl leading-relaxed text-foreground/90 italic font-medium">
                    "{analysis?.coachRemark || "You displayed a high degree of domain expertise throughout the session."}"
                  </p>
                </div>
              </div>
              <div className="mt-auto space-y-4 pt-8">
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
            {questions.map((q, i) => (
              <Card key={q.id} className="rounded-[2.5rem] border-2 border-border shadow-md hover:border-primary/20 transition-all overflow-hidden group">
                <CardHeader className="p-8 md:p-10 border-b border-border bg-card/30">
                  <div className="flex justify-between items-start gap-4">
                    <div className="flex gap-6">
                      <div className="w-12 h-12 rounded-2xl bg-secondary flex items-center justify-center font-black text-xl group-hover:scale-110 transition-transform">
                        {i + 1}
                      </div>
                      <div className="space-y-2">
                        <Badge variant="secondary" className="rounded-full px-3 py-1 font-black text-[10px] uppercase tracking-widest border-primary/10">
                          {q.score > 85 ? 'STRENGTH' : 'OPPORTUNITY'}
                        </Badge>
                        <CardTitle className="text-2xl font-black tracking-tight leading-snug">
                          {q.questionText}
                        </CardTitle>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-xs font-black text-muted-foreground uppercase tracking-widest mb-1">Score</p>
                      <p className={`text-3xl font-black ${q.score > 80 ? 'text-primary' : 'text-orange-500'}`}>{q.score}</p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="p-8 md:p-10 bg-background">
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                    <div className="space-y-4">
                      <p className="text-xs font-black text-muted-foreground uppercase tracking-widest">Your Response</p>
                      <p className="text-lg leading-relaxed text-muted-foreground font-medium">
                        "{q.userAnswer}"
                      </p>
                    </div>
                    <div className="bg-primary/5 rounded-[2rem] p-8 border border-primary/10">
                      <p className="text-xs font-black text-primary uppercase tracking-widest mb-4 flex items-center gap-2">
                        <Zap className="w-4 h-4 fill-primary" /> AI Coaching Tip
                      </p>
                      <p className="text-lg leading-relaxed font-bold">
                        {q.aiFeedback}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Footer CTA */}
        <section className="bg-card border-2 border-border rounded-[4rem] p-16 text-center animate-reveal [animation-delay:600ms]">
          <h2 className="text-4xl md:text-5xl font-black tracking-tighter mb-6">Feeling more confident?</h2>
          <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
            Consistency is key to mastering interviews. Schedule another simulation to practice your improvements and track your progress.
          </p>
          <Button size="lg" className="h-16 px-12 rounded-full text-xl font-black shadow-xl hover:scale-105 transition-transform">
            Try Another Simulation <ArrowRight className="ml-2 w-6 h-6" />
          </Button>
        </section>
      </main>
    </div>
  );
}
