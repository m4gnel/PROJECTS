import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAgent, useBlinkAuth } from '@blinkdotnew/react';
import { interviewCoachAgent } from '@/lib/agent';
import { blink } from '@/lib/blink';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Send, 
  Mic, 
  StopCircle, 
  ChevronLeft, 
  MoreHorizontal,
  Briefcase,
  AlertCircle,
  CheckCircle2,
  BrainCircuit,
  Loader2,
  Volume2,
  VolumeX
} from 'lucide-react';
import { toast } from 'react-hot-toast';

const ANALYZE_FUNCTION_URL = 'https://kwauxn5v--analyze-interview.functions.blink.new';

interface InterviewData {
  id: string;
  field: string;
  category: string;
  experienceLevel: string;
  status: string;
}

export function InterviewSession() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useBlinkAuth();
  const [interview, setInterview] = useState<InterviewData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isVoiceEnabled, setIsVoiceEnabled] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const speakText = async (text: string) => {
    if (!isVoiceEnabled) return;
    try {
      const audioUrl = await blink.ai.generateSpeech({
        text,
        voice: 'alloy' // Professional recruiter voice
      });
      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.play();
      } else {
        const audio = new Audio(audioUrl);
        audioRef.current = audio;
        audio.play();
      }
    } catch (error) {
      console.error('Speech generation failed:', error);
    }
  };

  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading: isAgentThinking,
    append,
    stop
  } = useAgent({
    agent: interviewCoachAgent,
    onFinish: (response) => {
      // Speak the AI's question
      speakText(response.text);
      
      // Check if the interview has concluded based on AI response
      if (response.text.toLowerCase().includes('interview has concluded')) {
        handleInterviewEnd();
      }
    }
  });

  // Track interview conclusion
  const [isConcluding, setIsConcluding] = useState(false);

  useEffect(() => {
    async function loadInterview() {
      if (!id) return;
      try {
        const data = await blink.db.interviews.get(id) as InterviewData;
        if (!data) {
          toast.error('Interview session not found');
          navigate('/dashboard');
          return;
        }
        setInterview(data);
        
        // Initialize the interview with a prompt
        const initialPrompt = `Hello Alex. I am ready for my interview for the position of ${data.field}. 
This is a ${data.category} interview. My experience level is ${data.experienceLevel}. 
Please start the interview by introducing yourself and asking me to introduce myself.`;
        
        append({
          role: 'user',
          content: initialPrompt,
          hidden: true // Custom property to hide system-init messages from UI if supported, or handle in render
        });

      } catch (error) {
        console.error('Failed to load interview:', error);
        toast.error('Error initializing session');
      } finally {
        setIsLoading(false);
      }
    }
    loadInterview();
  }, [id]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isAgentThinking]);

  const handleInterviewEnd = async () => {
    if (!id || isConcluding) return;
    setIsConcluding(true);
    
    try {
      toast.loading('Alex is finalising your performance review...', { id: 'concluding' });
      
      // Construct transcript
      const transcript = messages
        .filter(m => !m.hidden)
        .map(m => `${m.role.toUpperCase()}: ${m.content}`)
        .join('\n\n');

      // Call analysis function
      const response = await fetch(ANALYZE_FUNCTION_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${blink.auth.getValidToken()}`
        },
        body: JSON.stringify({
          transcript,
          field: interview?.field,
          experienceLevel: interview?.experienceLevel,
          category: interview?.category
        })
      });

      if (!response.ok) throw new Error('Analysis failed');
      
      const analysis = await response.json();

      // Update database with structured results
      await blink.db.interviews.update(id, {
        status: 'completed',
        score: analysis.overallScore,
        overallFeedback: analysis.coachRemark,
        analysisData: JSON.stringify(analysis) // Store full JSON for the report
      });

      // Also store individual questions
      if (analysis.questions && analysis.questions.length > 0) {
        await blink.db.questions.createMany(
          analysis.questions.map((q: any, index: number) => ({
            interviewId: id,
            questionText: q.question,
            userAnswer: q.answer,
            aiFeedback: q.feedback,
            score: q.score,
            orderIndex: index
          }))
        );
      }

      toast.success('Analysis complete! Redirecting to your report...', { id: 'concluding' });
      setTimeout(() => navigate(`/feedback/${id}`), 1500);
    } catch (error) {
      console.error('Failed to conclude interview:', error);
      toast.error('Error during performance analysis. Please try manually.', { id: 'concluding' });
      setIsConcluding(false);
    }
  };

  const endSessionEarly = () => {
    if (window.confirm('Are you sure you want to end this session? You will lose progress.')) {
      navigate('/dashboard');
    }
  };

  if (isLoading || !interview || isConcluding) {
    return (
      <div className="h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-primary animate-spin mx-auto mb-4" />
          <p className="text-xl font-bold">{isConcluding ? 'Alex is writing your feedback...' : 'Initializing Simulation...'}</p>
          <p className="text-muted-foreground">{isConcluding ? 'Processing STAR method analysis and communication scores' : 'Setting up your professional AI recruiter'}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-background overflow-hidden lg:flex-row">
      {/* Session Controls / Info */}
      <aside className="w-full lg:w-96 border-b lg:border-b-0 lg:border-r border-border p-8 glass-dark flex flex-col">
        <Button variant="ghost" className="w-fit mb-8 -ml-2 text-muted-foreground hover:text-foreground" onClick={() => navigate('/dashboard')}>
          <ChevronLeft className="mr-2 w-4 h-4" />
          Back to Dashboard
        </Button>

        <div className="mb-10">
          <Badge variant="secondary" className="mb-4 rounded-full px-4 py-1 text-xs font-black uppercase tracking-[0.2em] border-primary/20">LIVE SESSION</Badge>
          <h2 className="text-4xl font-black tracking-tighter mb-4 leading-tight">{interview.field}</h2>
          <div className="space-y-4">
            <div className="flex items-center gap-3 text-lg font-medium text-muted-foreground">
              <Briefcase className="w-5 h-5 text-primary" />
              {interview.category}
            </div>
            <div className="flex items-center gap-3 text-lg font-medium text-muted-foreground">
              <BrainCircuit className="w-5 h-5 text-primary" />
              {interview.experienceLevel}
            </div>
          </div>
        </div>

        <div className="mt-auto space-y-4 pt-8 border-t border-border">
          <Button 
            variant="outline" 
            className={`w-full h-14 rounded-2xl border-2 font-bold transition-all ${isVoiceEnabled ? 'text-primary border-primary/20 bg-primary/5' : 'text-muted-foreground border-border'}`}
            onClick={() => setIsVoiceEnabled(!isVoiceEnabled)}
          >
            {isVoiceEnabled ? <Volume2 className="mr-2 w-5 h-5" /> : <VolumeX className="mr-2 w-5 h-5" />}
            AI Voice: {isVoiceEnabled ? 'ON' : 'OFF'}
          </Button>

          <div className="bg-primary/5 rounded-2xl p-6 border border-primary/10">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <p className="font-bold text-sm text-primary uppercase tracking-widest">Recruiter Status</p>
            </div>
            <p className="text-base font-medium">Alex is {isAgentThinking ? 'listening and taking notes...' : 'waiting for your response'}</p>
          </div>
          
          <Button variant="outline" className="w-full h-14 rounded-2xl border-2 text-destructive hover:bg-destructive/5 font-bold" onClick={endSessionEarly}>
            <StopCircle className="mr-2 w-5 h-5" />
            End Session Early
          </Button>
        </div>
      </aside>

      {/* Interview Chat Canvas */}
      <main className="flex-1 flex flex-col relative bg-card/20 overflow-hidden">
        <div 
          ref={scrollRef}
          className="flex-1 overflow-y-auto p-6 md:p-12 space-y-8 scroll-smooth"
        >
          {messages.filter(m => !m.hidden).map((msg, i) => (
            <div 
              key={i} 
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-reveal`}
              style={{ animationDelay: `${i * 100}ms` }}
            >
              <div className={`max-w-[85%] md:max-w-[70%] flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-10 h-10 md:w-12 md:h-12 rounded-2xl flex-shrink-0 flex items-center justify-center shadow-lg ${msg.role === 'user' ? 'bg-secondary border border-border' : 'bg-primary shadow-primary/20'}`}>
                  {msg.role === 'user' ? (
                    <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user?.email}`} alt="User" className="w-full h-full rounded-2xl" />
                  ) : (
                    <Briefcase className="text-white w-6 h-6" />
                  )}
                </div>
                <div className={`space-y-2 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                  <p className="text-xs font-black text-muted-foreground uppercase tracking-widest">
                    {msg.role === 'user' ? 'You' : 'Alex (Recruiter)'}
                  </p>
                  <div className={`p-5 md:p-6 rounded-3xl text-lg md:text-xl leading-relaxed shadow-sm ${
                    msg.role === 'user' 
                      ? 'bg-primary text-primary-foreground rounded-tr-none' 
                      : 'glass border-primary/10 rounded-tl-none text-foreground'
                  }`}>
                    {msg.content}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {isAgentThinking && (
            <div className="flex justify-start animate-reveal">
              <div className="max-w-[85%] md:max-w-[70%] flex gap-4">
                <div className="w-10 h-10 md:w-12 md:h-12 rounded-2xl bg-primary flex-shrink-0 flex items-center justify-center animate-pulse shadow-lg shadow-primary/20">
                  <Briefcase className="text-white w-6 h-6" />
                </div>
                <div className="space-y-2">
                  <p className="text-xs font-black text-muted-foreground uppercase tracking-widest">Alex is thinking...</p>
                  <div className="glass p-5 rounded-3xl rounded-tl-none flex gap-2 items-center">
                    <span className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]" />
                    <span className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]" />
                    <span className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="p-6 md:p-10 bg-background/80 backdrop-blur-md border-t border-border relative z-30">
          <div className="max-w-4xl mx-auto flex gap-4">
            <div className="relative flex-1">
              <form onSubmit={handleSubmit}>
                <input
                  value={input}
                  onChange={handleInputChange}
                  placeholder="Type your answer here... (e.g. In my last role at X, I was responsible for...)"
                  className="w-full h-16 bg-secondary/50 border-2 border-border focus:border-primary rounded-[1.5rem] px-8 text-lg font-medium transition-all outline-none disabled:opacity-50"
                  disabled={isAgentThinking}
                />
                <button 
                  type="submit" 
                  disabled={!input.trim() || isAgentThinking}
                  className="absolute right-3 top-2.5 w-12 h-11 bg-primary text-white rounded-2xl flex items-center justify-center shadow-lg shadow-primary/30 hover:scale-105 active:scale-95 transition-all disabled:opacity-50"
                >
                  <Send className="w-5 h-5" />
                </button>
              </form>
            </div>
            <Button size="icon" variant="outline" className="w-16 h-16 rounded-[1.5rem] border-2 group hover:bg-primary/5 transition-all">
              <Mic className="w-7 h-7 text-primary group-hover:scale-110 transition-transform" />
            </Button>
          </div>
          <p className="text-center text-xs font-bold text-muted-foreground mt-4 uppercase tracking-[0.15em] opacity-60">
            Professional Tip: Use the STAR method for behavioral questions
          </p>
        </div>

        {/* Decorative canvas elements */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-[80px] pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-accent/5 rounded-full blur-[80px] pointer-events-none" />
      </main>
    </div>
  );
}
