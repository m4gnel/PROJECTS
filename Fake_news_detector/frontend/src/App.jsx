import React, { useState, useEffect, useRef } from 'react';
import Sidebar from './Sidebar';
import PromptCard from './PromptCard';
import QuickChips from './QuickChips';
import VerdictCard from './VerdictCard';
import PerformanceModal from './PerformanceModal';
import ArchitectureModal from './ArchitectureModal';
import ReportModal from './ReportModal';
import ToolsDrawer from './ToolsDrawer';
import SamplesDrawer from './SamplesDrawer';
import { predictArticleInference } from './nlpEngine';
import { INITIAL_PROJECTS, PROJECT_METADATA } from './modelData';
import { Sparkles, FileText, BarChart3, Layers, CheckCircle2 } from 'lucide-react';

export default function App() {
  const [collapsed, setCollapsed] = useState(false);
  const [projects, setProjects] = useState(INITIAL_PROJECTS);
  const [activeProject, setActiveProject] = useState('pirnjo');
  
  const [inputValue, setInputValue] = useState('');
  const [selectedModel, setSelectedModel] = useState('bilstm-optimal');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  // NLP Configuration
  const [nlpOptions, setNlpOptions] = useState({
    removeDateline: true,
    removeStopwords: true,
    applyLemmatizer: true,
    maxLen: 300
  });

  // Modals
  const [metricsModalOpen, setMetricsModalOpen] = useState(false);
  const [architectureModalOpen, setArchitectureModalOpen] = useState(false);
  const [reportModalOpen, setReportModalOpen] = useState(false);
  const [toolsDrawerOpen, setToolsDrawerOpen] = useState(false);
  const [samplesDrawerOpen, setSamplesDrawerOpen] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleVerify = (textToVerify = inputValue) => {
    const text = textToVerify.trim();
    if (!text) return;

    setIsLoading(true);

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');

    // Authentic inference pass with slight realistic latency
    setTimeout(() => {
      const result = predictArticleInference(text, nlpOptions);
      const assistantMessage = {
        id: Date.now() + 1,
        sender: 'assistant',
        result,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 450);
  };

  const handleNewChat = () => {
    setMessages([]);
    setInputValue('');
  };

  const handleQuickAction = (actionId) => {
    switch (actionId) {
      case 'deep_search':
        setInputValue('WASHINGTON (Reuters) - The Senate voted on Tuesday on 3 bills to expand federal infrastructure and semiconductor manufacturing investments across Midwestern states, according to official committee statements released by leadership.');
        break;
      case 'create_images':
        setInputValue('Breaking: scientists confirm the moon is made of cheese');
        break;
      case 'latest_news':
        setInputValue('Federal Reserve officials signaled on Wednesday that benchmark interest rate policies will remain tied to upcoming monthly consumer price index data and national labor market statistics, spokesman confirmed.');
        break;
      case 'generate_video':
        setArchitectureModalOpen(true);
        break;
      case 'metrics':
        setMetricsModalOpen(true);
        break;
      default:
        break;
    }
  };

  const handleSelectSample = (sampleText) => {
    setInputValue(sampleText);
    handleVerify(sampleText);
  };

  return (
    <div className="app-container">
      {/* Ambient background blur */}
      <div className="ambient-glow" />

      {/* Left Navigation Sidebar */}
      <Sidebar 
        collapsed={collapsed}
        setCollapsed={setCollapsed}
        projects={projects}
        activeProject={activeProject}
        setActiveProject={setActiveProject}
        onNewChat={handleNewChat}
        onOpenReport={() => setReportModalOpen(true)}
        onOpenMetrics={() => setMetricsModalOpen(true)}
        onOpenArchitecture={() => setArchitectureModalOpen(true)}
        onOpenSamples={() => setSamplesDrawerOpen(true)}
      />

      {/* Main Content View */}
      <main className="main-content">
        {/* Top Navbar */}
        <header className="top-bar-nav">
          <button 
            className="top-pill-btn accent" 
            onClick={() => setMetricsModalOpen(true)}
            title="Held-out Test Performance"
          >
            <BarChart3 size={13} />
            <span>99.36% Accuracy</span>
          </button>

          <button 
            className="top-pill-btn" 
            onClick={() => setArchitectureModalOpen(true)}
            title="BiLSTM 6-Layer Architecture"
          >
            <Layers size={13} />
            <span>BiLSTM Model (2.66M Params)</span>
          </button>

          <button 
            className="top-pill-btn" 
            onClick={() => setReportModalOpen(true)}
            title="KTU Course Project Report"
          >
            <FileText size={13} />
            <span>Course Project Report</span>
          </button>
        </header>

        {/* Center Container */}
        <div className="chat-container">
          {messages.length === 0 ? (
            /* Home State Matching Reference Screenshot */
            <div style={{ margin: 'auto 0', display: 'flex', flexDirection: 'column' }}>
              <div className="hero-section">
                <h1 className="hero-title">Hey, How Can I Assist?</h1>
                <p className="hero-subtitle">
                  AI Chat is our smartest and fastest deep learning fake news detector — built to give you accurate, explainable credibility scores every time.
                </p>
              </div>

              {/* Center Input Card */}
              <PromptCard 
                inputValue={inputValue}
                setInputValue={setInputValue}
                onSubmit={() => handleVerify()}
                isLoading={isLoading}
                selectedModel={selectedModel}
                setSelectedModel={setSelectedModel}
                onOpenTools={() => setToolsDrawerOpen(true)}
                onAttachSample={() => setSamplesDrawerOpen(true)}
              />

              {/* Quick Action Chips (Matches Screenshot) */}
              <QuickChips onSelectAction={handleQuickAction} />
            </div>
          ) : (
            /* Conversation Stream */
            <div style={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
              <div className="chat-messages-feed">
                {messages.map((msg) => (
                  <React.Fragment key={msg.id}>
                    {msg.sender === 'user' ? (
                      <div className="chat-bubble-user">
                        <div style={{ fontSize: '0.74rem', color: '#94a3b8', marginBottom: '4px', display: 'flex', justifyContent: 'space-between' }}>
                          <span>Submitted Article / Claim</span>
                          <span>{msg.timestamp}</span>
                        </div>
                        <p>{msg.text}</p>
                      </div>
                    ) : (
                      <div className="chat-bubble-assistant">
                        <VerdictCard 
                          result={msg.result}
                          onOpenMetrics={() => setMetricsModalOpen(true)}
                          onOpenArchitecture={() => setArchitectureModalOpen(true)}
                        />
                      </div>
                    )}
                  </React.Fragment>
                ))}

                {isLoading && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#94a3b8', padding: '12px' }}>
                    <div style={{ width: '16px', height: '16px', borderRadius: '50%', border: '2px solid #38bdf8', borderTopColor: 'transparent', animation: 'spin 1s linear infinite' }} />
                    <span style={{ fontSize: '0.86rem' }}>Running BiLSTM forward pass and token attribution...</span>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Sticky bottom input when chat is active */}
              <div style={{ marginTop: 'auto', paddingTop: '20px' }}>
                <PromptCard 
                  inputValue={inputValue}
                  setInputValue={setInputValue}
                  onSubmit={() => handleVerify()}
                  isLoading={isLoading}
                  selectedModel={selectedModel}
                  setSelectedModel={setSelectedModel}
                  onOpenTools={() => setToolsDrawerOpen(true)}
                  onAttachSample={() => setSamplesDrawerOpen(true)}
                />
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Modals & Overlays */}
      <PerformanceModal 
        isOpen={metricsModalOpen} 
        onClose={() => setMetricsModalOpen(false)} 
      />

      <ArchitectureModal 
        isOpen={architectureModalOpen} 
        onClose={() => setArchitectureModalOpen(false)} 
      />

      <ReportModal 
        isOpen={reportModalOpen} 
        onClose={() => setReportModalOpen(false)} 
      />

      <ToolsDrawer 
        isOpen={toolsDrawerOpen} 
        onClose={() => setToolsDrawerOpen(false)} 
        nlpOptions={nlpOptions}
        setNlpOptions={setNlpOptions}
      />

      <SamplesDrawer 
        isOpen={samplesDrawerOpen} 
        onClose={() => setSamplesDrawerOpen(false)} 
        onSelectSample={handleSelectSample}
      />
    </div>
  );
}
