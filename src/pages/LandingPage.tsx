import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { blink } from '@/lib/blink'
import { useBlinkAuth } from '@blinkdotnew/react'
import { useNavigate, Link } from 'react-router-dom'
import { 
  CheckCircle, 
  MessageSquare, 
  Target, 
  Zap, 
  ArrowRight, 
  ShieldCheck, 
  Sparkles,
  BrainCircuit,
  Star,
  TrendingUp,
  Globe
} from 'lucide-react'

export function LandingPage() {
  const { isAuthenticated } = useBlinkAuth()
  const navigate = useNavigate()

  const handleCTA = () => {
    if (isAuthenticated) {
      navigate('/dashboard')
    } else {
      blink.auth.login(window.location.origin + '/dashboard')
    }
  }

  const features = [
    {
      title: 'Adaptive AI Recruiter',
      description: 'Our AI adjusts its questioning style based on your responses, just like a real senior interviewer.',
      icon: BrainCircuit,
    },
    {
      title: 'STAR Method Analysis',
      description: 'Get deep analysis of your behavioral answers using the Situation, Task, Action, Result framework.',
      icon: Star,
    },
    {
      title: 'Domain Expertise',
      description: 'Questions tailored for 500+ roles across tech, finance, health, and creative industries.',
      icon: Target,
    },
    {
      title: 'Instant Scoring',
      description: 'Receive a detailed scorecard on your communication, technical depth, and overall impact.',
      icon: Zap,
    },
    {
      title: 'Progress Tracking',
      description: 'Visualize your growth with detailed analytics over multiple interview sessions.',
      icon: TrendingUp,
    },
    {
      title: 'Global Standards',
      description: 'Prepare for interviews in 20+ languages following international recruitment standards.',
      icon: Globe,
    }
  ];

  return (
    <div className="flex flex-col min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden hero-gradient">
        <div className="container relative z-10 px-6">
          <div className="mx-auto max-w-5xl text-center">
            <Badge variant="secondary" className="mb-6 animate-reveal py-1.5 px-4 text-sm font-medium tracking-wide glass border-primary/20">
              <Sparkles className="mr-2 h-4 w-4 text-primary" />
              Trusted by 50,000+ Professionals
            </Badge>
            <h1 className="mb-8 text-6xl font-bold tracking-tight text-foreground sm:text-7xl lg:text-8xl animate-reveal leading-[1.05]">
              Land your dream job with <br />
              <span className="text-primary text-glow italic">AI-powered</span> practice
            </h1>
            <p className="mx-auto mb-12 max-w-2xl text-lg text-muted-foreground sm:text-xl animate-reveal [animation-delay:200ms]">
              The most advanced AI interview coach. Realistic simulations, instant behavioral analysis, 
              and tailored feedback that blows your mind.
            </p>
            <div className="flex flex-col items-center justify-center gap-6 sm:flex-row animate-reveal [animation-delay:400ms]">
              <Button size="lg" className="h-16 px-10 text-xl font-bold rounded-full group shadow-2xl hover:shadow-primary/30 transition-all" onClick={handleCTA}>
                Start Training Free <ArrowRight className="ml-2 h-6 w-6 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button size="lg" variant="outline" className="h-16 px-10 text-xl font-bold rounded-full border-2 glass hover:bg-secondary/50">
                View Sample Report
              </Button>
            </div>

            <div className="mt-24 flex flex-wrap justify-center items-center gap-10 md:gap-16 opacity-40 grayscale animate-reveal [animation-delay:600ms]">
              <span className="text-2xl font-bold tracking-tighter">GOOGLE</span>
              <span className="text-2xl font-bold tracking-tighter">AMAZON</span>
              <span className="text-2xl font-bold tracking-tighter">MICROSOFT</span>
              <span className="text-2xl font-bold tracking-tighter">STRIPE</span>
              <span className="text-2xl font-bold tracking-tighter">MCKINSEY</span>
            </div>
          </div>
        </div>

        {/* Abstract Glow Elements */}
        <div className="absolute top-1/4 -left-64 w-[600px] h-[600px] bg-primary/10 rounded-full blur-[120px] animate-float" />
        <div className="absolute bottom-1/4 -right-64 w-[600px] h-[600px] bg-accent/10 rounded-full blur-[120px] animate-float [animation-delay:2s]" />
      </section>

      {/* Feature Grid */}
      <section className="py-32 bg-secondary/30 relative">
        <div className="container px-6 relative z-10">
          <div className="mb-20 text-center max-w-3xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-6">Master every aspect of the interview</h2>
            <p className="text-lg text-muted-foreground">Comprehensive training modules designed to prepare you for high-stakes conversations.</p>
          </div>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, i) => (
              <div 
                key={i} 
                className="group glass p-10 rounded-[2rem] transition-all hover:-translate-y-2 hover:shadow-2xl border-transparent hover:border-primary/20 animate-reveal"
                style={{ animationDelay: `${i * 100}ms` }}
              >
                <div className="mb-8 inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 text-primary group-hover:scale-110 group-hover:bg-primary group-hover:text-primary-foreground transition-all">
                  <feature.icon className="h-7 w-7" />
                </div>
                <h3 className="mb-4 text-2xl font-bold tracking-tight">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-32 overflow-hidden">
        <div className="container px-6">
          <div className="flex flex-col md:flex-row items-end justify-between mb-16 gap-8">
            <div className="max-w-2xl">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Success stories from our community</h2>
              <p className="text-lg text-muted-foreground">Join thousands of professionals who successfully changed their lives.</p>
            </div>
            <Button variant="ghost" className="text-primary font-bold gap-2 hover:bg-primary/5">
              Read all testimonials <ArrowRight className="h-5 w-5" />
            </Button>
          </div>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {[
              {
                name: "Alex Rivera",
                role: "Senior PM at Meta",
                content: "The feedback was brutal but exactly what I needed. I landed my Meta offer after 4 practice sessions here.",
                image: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop"
              },
              {
                name: "Priya Sharma",
                role: "UX Lead at Airbnb",
                content: "It felt like talking to a real human recruiter. The follow-up questions were remarkably intelligent and deep.",
                image: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop"
              },
              {
                name: "David Kim",
                role: "Software Engineer at Netflix",
                content: "Best interview prep tool I've ever used. The technical depth analysis is second to none.",
                image: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&h=100&fit=crop"
              }
            ].map((t, i) => (
              <div key={i} className="p-10 rounded-3xl bg-card border border-border shadow-sm hover:shadow-md transition-shadow">
                <div className="flex gap-1 mb-6">
                  {[...Array(5)].map((_, j) => (
                    <Star key={j} className="h-5 w-5 fill-primary text-primary" />
                  ))}
                </div>
                <p className="text-xl leading-relaxed mb-8">"{t.content}"</p>
                <div className="flex items-center gap-4">
                  <img src={t.image} alt={t.name} className="h-12 w-12 rounded-full object-cover" />
                  <div>
                    <h4 className="font-bold">{t.name}</h4>
                    <p className="text-sm text-muted-foreground">{t.role}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-32 container px-6">
        <div className="relative rounded-[4rem] bg-primary p-12 md:p-24 overflow-hidden shadow-3xl">
          <div className="relative z-10 max-w-3xl">
            <h2 className="text-4xl md:text-6xl font-bold text-primary-foreground mb-8 tracking-tighter">
              Ready to crush your <br className="hidden md:block" /> next interview?
            </h2>
            <p className="text-xl text-primary-foreground/80 mb-12 max-w-xl">
              Get started for free today. No credit card required. Master your skills in minutes.
            </p>
            <Button size="lg" variant="secondary" className="h-16 px-12 text-xl font-bold rounded-full hover:scale-105 transition-transform shadow-xl" onClick={handleCTA}>
              Start Practice Now
            </Button>
          </div>
          {/* Background Decorative Element */}
          <div className="absolute top-0 right-0 p-12 opacity-10">
            <BrainCircuit className="h-96 w-96 rotate-12" />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-20 border-t border-border bg-card">
        <div className="container px-6 grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 mb-6">
              <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
                <BrainCircuit className="text-white w-6 h-6" />
              </div>
              <span className="font-bold text-2xl tracking-tight">InterviewCoach AI</span>
            </div>
            <p className="text-muted-foreground text-lg max-w-md">
              The professional standard in AI interview preparation. Empowering candidates to land their dream roles with cutting-edge technology.
            </p>
          </div>
          <div>
            <h4 className="font-bold text-lg mb-6">Product</h4>
            <ul className="space-y-4 text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">How it works</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Pricing</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Success Stories</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Enterprise</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-lg mb-6">Company</h4>
            <ul className="space-y-4 text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">About Us</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Careers</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Terms of Service</a></li>
            </ul>
          </div>
        </div>
        <div className="container px-6 flex flex-col md:flex-row justify-between items-center gap-6 pt-12 border-t border-border text-muted-foreground">
          <p>© 2026 InterviewCoach AI. All rights reserved.</p>
          <div className="flex gap-8">
            <Globe className="h-5 w-5 hover:text-primary cursor-pointer" />
            <span className="h-5 w-5 hover:text-primary cursor-pointer">𝕏</span>
            <span className="h-5 w-5 hover:text-primary cursor-pointer">in</span>
          </div>
        </div>
      </footer>
    </div>
  )
}

