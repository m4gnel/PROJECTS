// =================================
// GLOBAL CONFIGURATION & STATE
// =================================
const API_BASE = (window.location.port === '5000' || window.location.hostname === 'localhost' && window.location.port === '5000') 
    ? '' 
    : 'http://localhost:5000';

const state = {
    currentPage: 'overview',
    currentQuestion: 1,
    totalQuestions: 5,
    timer: 0,
    timerInterval: null,
    userAnswers: [],
    currentInterview: null,
    selectedLibraryQuestion: null,
    scores: [],
    isLiveApi: false,
    isRecording: false,
    speechRecognition: null,
    charts: {}
};

// Curated question bank for standalone / offline resilience
const CURATED_QUESTIONS = [
    {
        id: 'q-tech-1',
        text: "Explain the difference between let, const, and var in JavaScript. When would you use each?",
        difficulty: "medium",
        category: "technical",
        field: "software",
        hint: "Think about block scope, variable hoisting, temporal dead zone, and reassignment rules."
    },
    {
        id: 'q-tech-2',
        text: "What is closure in JavaScript? Provide a concrete, real-world scenario where closures solve a state encapsulation challenge.",
        difficulty: "medium",
        category: "technical",
        field: "software",
        hint: "Consider private variables in factory functions or maintaining state in asynchronous callbacks."
    },
    {
        id: 'q-tech-3',
        text: "Describe the event loop in JavaScript and explain how microtasks (promises) and macrotasks (timers) are prioritized in the execution queue.",
        difficulty: "hard",
        category: "technical",
        field: "software",
        hint: "Trace call stack execution, web APIs, microtask queue resolution, and rendering steps."
    },
    {
        id: 'q-tech-4',
        text: "What is the difference between SQL and NoSQL databases? When would you choose PostgreSQL over MongoDB?",
        difficulty: "medium",
        category: "technical",
        field: "software",
        hint: "Compare relational schemas, ACID compliance, data consistency, scalability, and query complexity."
    },
    {
        id: 'q-behav-1',
        text: "Tell me about a time when you had to work with a difficult team member or stakeholder. How did you handle the situation and what was the outcome?",
        difficulty: "medium",
        category: "behavioral",
        field: "general",
        hint: "Structure your response using STAR: Situation, Task, Action, and quantifiable Result."
    },
    {
        id: 'q-behav-2',
        text: "Describe a project where requirements shifted dramatically under a tight deadline. How did you adapt your architecture and deliver results?",
        difficulty: "hard",
        category: "behavioral",
        field: "general",
        hint: "Focus on proactive communication, task prioritization, managing trade-offs, and lessons learned."
    },
    {
        id: 'q-behav-3',
        text: "Give an example of a mistake or failure in your engineering work. How did you take ownership and prevent it from recurring?",
        difficulty: "medium",
        category: "behavioral",
        field: "general",
        hint: "Demonstrate self-awareness, post-mortem methodology, automated testing, or process safeguards."
    },
    {
        id: 'q-sys-1',
        text: "Design a scalable URL shortening service like bit.ly capable of handling 100M active URLs and 10,000 requests per second.",
        difficulty: "hard",
        category: "system-design",
        field: "software",
        hint: "Discuss hashing algorithms (Base62), database sharding, caching tiers (Redis), and global CDN routing."
    },
    {
        id: 'q-sys-2',
        text: "Design a real-time collaborative document editing platform like Google Docs. Consider concurrency control and state synchronization.",
        difficulty: "hard",
        category: "system-design",
        field: "software",
        hint: "Evaluate Operational Transformation (OT) versus Conflict-free Replicated Data Types (CRDTs)."
    },
    {
        id: 'q-hr-1',
        text: "Why are you interested in joining our company, and what unique value will you bring to our team?",
        difficulty: "easy",
        category: "hr",
        field: "general",
        hint: "Align company mission, recent product achievements, and your personal growth trajectory."
    },
    {
        id: 'q-hr-2',
        text: "Where do you envision yourself professionally in the next 3 to 5 years?",
        difficulty: "easy",
        category: "hr",
        field: "general",
        hint: "Balance high ambition with practical skill acquisition, mentorship, and domain mastery."
    }
];

// =================================
// INITIALIZATION
// =================================
document.addEventListener('DOMContentLoaded', async function() {
    initNavigation();
    initMobileMenu();
    initPricingToggle();
    initVideoModal();
    initDashboard();
    initUserMenu();
    initSpeechRecognition();
    checkAuth();
    loadUserData();
    
    // Check backend health & connectivity
    await checkBackendHealth();
    
    // Populate dynamic screens
    loadOverviewStats();
    loadQuestionLibrary();
    loadPastSessions();
    
    // Initialize charts if on dashboard
    if (document.getElementById('performanceChart')) {
        initCharts();
    }
});

// =================================
// BACKEND CONNECTIVITY CHECK
// =================================
async function checkBackendHealth() {
    const badge = document.getElementById('apiStatusBadge');
    const textEl = document.getElementById('apiStatusText');
    
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2500);
        
        const res = await fetch(`${API_BASE}/health`, {
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        
        if (res.ok) {
            state.isLiveApi = true;
            if (badge) {
                badge.className = 'api-status-badge live';
                if (textEl) textEl.textContent = 'AI Engine Live';
            }
            console.log('⚡ Connected to AI Interview Coach Backend API');
            return true;
        }
    } catch (e) {
        // Backend not running - graceful offline fallback
    }
    
    state.isLiveApi = false;
    if (badge) {
        badge.className = 'api-status-badge offline';
        if (textEl) textEl.textContent = 'Demo Mode (Offline)';
    }
    console.log('💡 Running in Demo / Standalone Mode');
    return false;
}

// =================================
// AUTHENTICATION
// =================================
function checkAuth() {
    const authToken = localStorage.getItem('authToken');
    const currentPath = window.location.pathname;
    
    if (currentPath.includes('dashboard.html') && !authToken) {
        // Allow demo review on dashboard even without token
        localStorage.setItem('authToken', 'demo-guest-' + Date.now());
        localStorage.setItem('userEmail', 'alex.candidate@example.com');
        localStorage.setItem('userData', JSON.stringify({
            firstName: 'Alex',
            lastName: 'Candidate',
            email: 'alex.candidate@example.com'
        }));
    }
    
    if ((currentPath.includes('login.html') || currentPath.includes('signup.html')) && authToken) {
        const rememberMe = localStorage.getItem('rememberMe');
        if (rememberMe === 'true') {
            window.location.href = 'dashboard.html';
        }
    }
}

function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('rememberMe');
    window.location.href = 'index.html';
}

function loadUserData() {
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    const userEmail = localStorage.getItem('userEmail') || 'alex@example.com';
    
    const userNameElements = document.querySelectorAll('.user-name');
    const userAvatarElements = document.querySelectorAll('.user-avatar');
    
    const fullName = (userData.firstName && userData.lastName) 
        ? `${userData.firstName} ${userData.lastName}` 
        : (userEmail.split('@')[0].charAt(0).toUpperCase() + userEmail.split('@')[0].slice(1));
        
    const initials = (userData.firstName && userData.lastName)
        ? `${userData.firstName[0]}${userData.lastName[0]}`.toUpperCase()
        : userEmail.substring(0, 2).toUpperCase();
        
    userNameElements.forEach(el => el.textContent = fullName);
    userAvatarElements.forEach(el => el.textContent = initials);
}

// =================================
// NAVIGATION & PAGE SWITCHING
// =================================
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId.startsWith('#')) {
                e.preventDefault();
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
                const targetSection = document.querySelector(targetId);
                if (targetSection) {
                    targetSection.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
}

function initMobileMenu() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
}

function initDashboard() {
    const navItems = document.querySelectorAll('.nav-item');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const pageName = this.getAttribute('data-page');
            showPage(pageName);
        });
    });
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Voice mode radio change handler
    document.querySelectorAll('input[name="mode"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const voiceControls = document.querySelector('.voice-controls');
            if (voiceControls) {
                voiceControls.style.display = (this.value === 'voice') ? 'flex' : 'none';
            }
        });
    });
    
    // Voice record button handler
    const recordBtn = document.getElementById('recordBtn');
    if (recordBtn) {
        recordBtn.addEventListener('click', toggleVoiceRecording);
    }
}

function showPage(pageName) {
    const navItems = document.querySelectorAll('.nav-item');
    const pages = document.querySelectorAll('.page');
    
    navItems.forEach(i => {
        if (i.getAttribute('data-page') === pageName) {
            i.classList.add('active');
        } else {
            i.classList.remove('active');
        }
    });
    
    pages.forEach(p => p.classList.remove('active'));
    const targetPage = document.getElementById(pageName + 'Page');
    if (targetPage) {
        targetPage.classList.add('active');
        state.currentPage = pageName;
        
        // Re-render components for specific pages
        if (pageName === 'analytics') {
            initCharts();
        } else if (pageName === 'library') {
            loadQuestionLibrary();
        } else if (pageName === 'sessions') {
            loadPastSessions();
        } else if (pageName === 'overview') {
            loadOverviewStats();
        }
    }
}

function initUserMenu() {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    if (userMenuBtn && userDropdown) {
        userMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });
        document.addEventListener('click', function() {
            userDropdown.classList.remove('show');
        });
    }
}

function initPricingToggle() {
    const pricingToggle = document.getElementById('pricingToggle');
    const monthlyPrices = document.querySelectorAll('.monthly-price');
    const annualPrices = document.querySelectorAll('.annual-price');
    
    if (pricingToggle) {
        pricingToggle.addEventListener('change', function() {
            if (this.checked) {
                monthlyPrices.forEach(el => el.style.display = 'none');
                annualPrices.forEach(el => el.style.display = 'inline');
            } else {
                monthlyPrices.forEach(el => el.style.display = 'inline');
                annualPrices.forEach(el => el.style.display = 'none');
            }
        });
    }
}

function initVideoModal() {
    const modal = document.getElementById('videoModal');
    if (modal) {
        window.addEventListener('click', function(event) {
            if (event.target === modal) {
                closeVideo();
            }
        });
    }
}

function playVideo() {
    const modal = document.getElementById('videoModal');
    if (modal) modal.style.display = 'flex';
}

function closeVideo() {
    const modal = document.getElementById('videoModal');
    if (modal) {
        modal.style.display = 'none';
        const iframe = modal.querySelector('iframe');
        if (iframe) {
            const src = iframe.src;
            iframe.src = src;
        }
    }
}

// =================================
// WEB SPEECH RECOGNITION (VOICE MODE)
// =================================
function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        state.speechRecognition = new SpeechRecognition();
        state.speechRecognition.continuous = true;
        state.speechRecognition.interimResults = true;
        state.speechRecognition.lang = 'en-US';
        
        state.speechRecognition.onresult = function(event) {
            const answerBox = document.getElementById('answerBox');
            if (!answerBox) return;
            
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript + ' ';
                }
            }
            if (finalTranscript) {
                answerBox.value = (answerBox.value ? answerBox.value + ' ' : '') + finalTranscript.trim();
            }
        };
        
        state.speechRecognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            stopVoiceRecording();
            showToast('Voice input paused: ' + event.error, 'info');
        };
        
        state.speechRecognition.onend = function() {
            if (state.isRecording) {
                try { state.speechRecognition.start(); } catch (e) {}
            }
        };
    }
}

function toggleVoiceRecording() {
    if (!state.speechRecognition) {
        showToast('Speech recognition is not supported in this browser. Please type your answer.', 'error');
        return;
    }
    
    if (state.isRecording) {
        stopVoiceRecording();
    } else {
        startVoiceRecording();
    }
}

function startVoiceRecording() {
    if (!state.speechRecognition) return;
    try {
        state.speechRecognition.start();
        state.isRecording = true;
        const recordBtn = document.getElementById('recordBtn');
        if (recordBtn) {
            recordBtn.className = 'voice-btn recording';
            recordBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Recording (Listening...)';
        }
        showToast('Listening... Speak your answer clearly.', 'info');
    } catch (e) {
        console.error('Could not start recognition:', e);
    }
}

function stopVoiceRecording() {
    if (!state.speechRecognition) return;
    try {
        state.isRecording = false;
        state.speechRecognition.stop();
        const recordBtn = document.getElementById('recordBtn');
        if (recordBtn) {
            recordBtn.className = 'voice-btn';
            recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
        }
    } catch (e) {}
}

// =================================
// INTERVIEW LIFECYCLE
// =================================
function quickStartInterview(type) {
    showPage('practice');
    setTimeout(() => {
        const typeButtons = document.querySelectorAll('.option-btn');
        typeButtons.forEach(btn => {
            btn.classList.remove('active');
            if (btn.getAttribute('data-type') === type) {
                btn.classList.add('active');
            }
        });
        
        // Auto select field and level if not set
        const fieldEl = document.getElementById('field');
        const levelEl = document.getElementById('level');
        if (fieldEl && !fieldEl.value) fieldEl.value = 'software';
        if (levelEl && !levelEl.value) levelEl.value = 'intermediate';
    }, 150);
}

function startNewInterview() {
    quickStartInterview('technical');
}

async function startInterview() {
    const field = document.getElementById('field')?.value || 'software';
    const level = document.getElementById('level')?.value || 'intermediate';
    const selectedType = document.querySelector('.option-btn.active')?.getAttribute('data-type') || 'technical';
    const selectedMode = document.querySelector('input[name="mode"]:checked')?.value || 'text';
    const company = document.getElementById('company')?.value || 'general';
    
    const startBtn = document.getElementById('startBtn');
    const originalText = startBtn ? startBtn.innerHTML : '';
    if (startBtn) {
        startBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Initializing AI Session...';
        startBtn.disabled = true;
    }
    
    try {
        let interviewId = 'local-' + Date.now();
        
        // Start interview in backend if live
        if (state.isLiveApi) {
            try {
                const token = localStorage.getItem('authToken');
                const headers = { 'Content-Type': 'application/json' };
                if (token) headers['Authorization'] = `Bearer ${token}`;
                
                const res = await fetch(`${API_BASE}/api/interviews/start`, {
                    method: 'POST',
                    headers,
                    body: JSON.stringify({
                        field,
                        level,
                        type: selectedType,
                        company,
                        mode: selectedMode,
                        questionsTotal: state.totalQuestions
                    })
                });
                if (res.ok) {
                    const data = await res.json();
                    interviewId = data.interview.id;
                }
            } catch (e) {
                console.warn('Could not register interview in backend, continuing locally', e);
            }
        }
        
        // Fetch or assign question
        let question = state.selectedLibraryQuestion;
        if (!question) {
            question = await fetchQuestion(field, level, selectedType);
        }
        state.selectedLibraryQuestion = null; // Reset single question queue
        
        // Setup interview state
        state.currentInterview = {
            id: interviewId,
            field,
            level,
            type: selectedType,
            mode: selectedMode,
            startTime: Date.now(),
            currentQuestionData: question
        };
        
        // Switch view to active practice screen
        document.querySelector('.setup-card').style.display = 'none';
        document.getElementById('interviewScreen').style.display = 'block';
        
        // Toggle voice controls based on mode
        const voiceControls = document.querySelector('.voice-controls');
        if (voiceControls) {
            voiceControls.style.display = (selectedMode === 'voice') ? 'flex' : 'none';
        }
        
        displayQuestion(question);
        startTimer();
        
    } catch (error) {
        console.error('Error starting interview:', error);
        showToast('Failed to start interview. Please try again.', 'error');
    } finally {
        if (startBtn) {
            startBtn.innerHTML = originalText;
            startBtn.disabled = false;
        }
    }
}

async function fetchQuestion(field, level, type) {
    if (state.isLiveApi) {
        try {
            const res = await fetch(`${API_BASE}/api/questions/random`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ field, level, type })
            });
            if (res.ok) {
                const data = await res.json();
                return data.question;
            }
        } catch (e) {
            console.warn('Random question API call failed, using curated bank', e);
        }
    }
    
    // Curated question fallback
    const filtered = CURATED_QUESTIONS.filter(q => q.category === type || q.category === 'technical');
    const pick = filtered[Math.floor(Math.random() * filtered.length)] || CURATED_QUESTIONS[0];
    return pick;
}

function displayQuestion(question) {
    const questionText = document.getElementById('questionText');
    const currentQuestionEl = document.getElementById('currentQuestion');
    const totalQuestionsEl = document.getElementById('totalQuestions');
    
    if (questionText) questionText.textContent = question.text;
    if (currentQuestionEl) currentQuestionEl.textContent = state.currentQuestion;
    if (totalQuestionsEl) totalQuestionsEl.textContent = state.totalQuestions;
    
    const difficultyBadge = document.querySelector('.difficulty-badge');
    if (difficultyBadge) {
        const diff = question.difficulty || 'medium';
        difficultyBadge.className = `difficulty-badge ${diff}`;
        difficultyBadge.textContent = diff.charAt(0).toUpperCase() + diff.slice(1);
    }
    
    const categoryBadge = document.querySelector('.category-badge');
    if (categoryBadge) {
        const cat = question.category || state.currentInterview?.type || 'Technical';
        categoryBadge.textContent = cat.charAt(0).toUpperCase() + cat.slice(1);
    }
    
    // Store current question data
    if (state.currentInterview) {
        state.currentInterview.currentQuestionData = question;
    }
}

function startTimer() {
    state.timer = 0;
    const timerElement = document.getElementById('timer');
    if (state.timerInterval) clearInterval(state.timerInterval);
    
    state.timerInterval = setInterval(() => {
        state.timer++;
        const minutes = Math.floor(state.timer / 60);
        const seconds = state.timer % 60;
        if (timerElement) {
            timerElement.textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
    }, 1000);
}

function stopTimer() {
    if (state.timerInterval) {
        clearInterval(state.timerInterval);
        state.timerInterval = null;
    }
}

async function submitAnswer() {
    const answerBox = document.getElementById('answerBox');
    const answer = answerBox?.value.trim();
    
    if (!answer) {
        showToast('Please provide an answer before submitting', 'error');
        return;
    }
    
    stopVoiceRecording();
    
    const submitBtn = document.getElementById('submitAnswer');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> AI Evaluating Response...';
    submitBtn.disabled = true;
    
    try {
        const question = state.currentInterview?.currentQuestionData;
        const feedback = await analyzeAnswer(answer, question);
        
        state.userAnswers.push({
            questionNumber: state.currentQuestion,
            questionText: question ? question.text : 'Interview Question',
            category: question ? question.category : 'technical',
            answer: answer,
            feedback: feedback,
            timeSpent: state.timer
        });
        
        displayFeedback(feedback);
        document.querySelector('.answer-section').style.display = 'none';
        
    } catch (error) {
        console.error('Answer analysis error:', error);
        showToast('Failed to analyze answer. Please try again.', 'error');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

async function analyzeAnswer(answer, question) {
    if (state.isLiveApi) {
        try {
            const token = localStorage.getItem('authToken');
            const headers = { 'Content-Type': 'application/json' };
            if (token) headers['Authorization'] = `Bearer ${token}`;
            
            const res = await fetch(`${API_BASE}/api/answers/submit`, {
                method: 'POST',
                headers,
                body: JSON.stringify({
                    interviewId: state.currentInterview?.id,
                    questionId: question?.id,
                    questionText: question?.text,
                    answer: answer,
                    timeSpent: state.timer
                })
            });
            if (res.ok) {
                const data = await res.json();
                return data.feedback;
            }
        } catch (e) {
            console.warn('API answer submission error, using heuristic engine', e);
        }
    }
    
    // Heuristic AI Analysis
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const words = answer.split(/\s+/).length;
    let score = 7.0;
    const strengths = [];
    const improvements = [];
    
    if (words > 80) {
        score += 1.5;
        strengths.push("Comprehensive elaboration demonstrating depth of subject knowledge");
    } else if (words > 40) {
        score += 0.8;
        strengths.push("Clear and concise core explanation");
    } else {
        improvements.push("Expand your response with more specific architectural details and trade-offs");
    }
    
    const lower = answer.toLowerCase();
    if (lower.includes('for example') || lower.includes('such as') || lower.includes('in my project')) {
        score += 0.8;
        strengths.push("Effective use of concrete, practical examples to substantiate points");
    } else {
        improvements.push("Include a real-world scenario or project experience to reinforce your reasoning");
    }
    
    if (lower.includes('because') || lower.includes('therefore') || lower.includes('however') || lower.includes('trade-off')) {
        strengths.push("Strong logical transitions and analytical structure");
    } else {
        improvements.push("Discuss alternative approaches and compare trade-offs");
    }
    
    score = Math.min(9.8, Math.max(5.0, score));
    
    return {
        score: parseFloat(score.toFixed(1)),
        technical_accuracy: parseFloat(Math.min(10, score + 0.2).toFixed(1)),
        communication_clarity: parseFloat(Math.min(10, score + 0.4).toFixed(1)),
        depth_of_knowledge: parseFloat(Math.min(10, score - 0.2).toFixed(1)),
        strengths: strengths.length ? strengths : ["Addressed the prompt directly", "Professional tone and vocabulary"],
        improvements: improvements.length ? improvements : ["Elaborate on edge cases", "Highlight quantifiable performance impact"],
        detailedFeedback: `Your response demonstrates solid foundational competence. ${strengths[0] || 'You answered directly.'} To take this answer to top-tier benchmark level, ${improvements[0]?.toLowerCase() || 'continue providing clear examples.'}`
    };
}

function displayFeedback(feedback) {
    const feedbackSection = document.getElementById('feedbackSection');
    const feedbackContent = document.getElementById('feedbackContent');
    
    if (feedbackSection && feedbackContent) {
        feedbackContent.innerHTML = `
            <div class="feedback-strengths">
                <h4><i class="fas fa-check-circle" style="color: var(--success);"></i> Strengths</h4>
                <ul>
                    ${(feedback.strengths || []).map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
            
            <div class="feedback-improvements" style="margin-top: 1.25rem;">
                <h4><i class="fas fa-lightbulb" style="color: var(--warning);"></i> Areas for Improvement</h4>
                <ul>
                    ${(feedback.improvements || []).map(i => `<li>${i}</li>`).join('')}
                </ul>
            </div>
            
            <div class="feedback-detailed" style="margin-top: 1.25rem;">
                <h4><i class="fas fa-comment-dots" style="color: var(--primary);"></i> AI Coach Analysis</h4>
                <p style="color: var(--text-secondary); line-height: 1.8;">${feedback.detailedFeedback || feedback.detailed_feedback || 'Well-structured response.'}</p>
            </div>
        `;
        
        const scoreBadge = feedbackSection.querySelector('.score-badge');
        if (scoreBadge) {
            scoreBadge.textContent = `${feedback.score}/10`;
        }
        
        feedbackSection.style.display = 'block';
    }
}

async function nextQuestion() {
    state.currentQuestion++;
    
    if (state.currentQuestion > state.totalQuestions) {
        await completeInterview();
    } else {
        resetQuestionScreen();
        
        // Fetch next adaptive question
        const question = await fetchQuestion(
            state.currentInterview?.field || 'software',
            state.currentInterview?.level || 'intermediate',
            state.currentInterview?.type || 'technical'
        );
        displayQuestion(question);
        startTimer();
    }
}

function skipQuestion() {
    if (confirm('Are you sure you want to skip this question?')) {
        nextQuestion();
    }
}

function endInterview() {
    if (confirm('Are you sure you want to end the interview now? Your completed answers will be saved.')) {
        completeInterview();
    }
}

async function completeInterview() {
    stopTimer();
    stopVoiceRecording();
    
    let avgScore = 8.0;
    if (state.userAnswers.length > 0) {
        const total = state.userAnswers.reduce((sum, ans) => sum + (ans.feedback?.score || 7.0), 0);
        avgScore = parseFloat((total / state.userAnswers.length).toFixed(1));
    }
    
    const sessionRecord = {
        id: state.currentInterview?.id || 'session-' + Date.now(),
        date: new Date().toISOString(),
        score: avgScore,
        type: state.currentInterview?.type || 'technical',
        field: state.currentInterview?.field || 'software',
        questionsAnswered: state.userAnswers.length,
        durationSeconds: state.timer,
        answers: state.userAnswers
    };
    
    // Save to local storage
    const savedSessions = JSON.parse(localStorage.getItem('interviewScores') || '[]');
    savedSessions.unshift(sessionRecord);
    localStorage.setItem('interviewScores', JSON.stringify(savedSessions));
    
    // Complete in backend if live
    if (state.isLiveApi && state.currentInterview?.id && !state.currentInterview.id.startsWith('local-')) {
        try {
            const token = localStorage.getItem('authToken');
            const headers = { 'Content-Type': 'application/json' };
            if (token) headers['Authorization'] = `Bearer ${token}`;
            
            await fetch(`${API_BASE}/api/interviews/${state.currentInterview.id}/complete`, {
                method: 'POST',
                headers,
                body: JSON.stringify({
                    score: avgScore,
                    duration: state.timer,
                    questionsAnswered: state.userAnswers.length
                })
            });
        } catch (e) {
            console.warn('Backend interview completion error', e);
        }
    }
    
    // Show results
    showResultsModal(avgScore);
    resetInterview();
    loadOverviewStats();
    loadPastSessions();
}

function showResultsModal(score) {
    const modal = document.getElementById('resultsModal');
    if (!modal) return;
    
    const scoreText = modal.querySelector('.score-text');
    if (scoreText) scoreText.innerHTML = `${score}<span>/10</span>`;
    
    const scoreProgress = modal.querySelector('.score-progress');
    if (scoreProgress) {
        const circumference = 283;
        const offset = circumference - (score / 10) * circumference;
        scoreProgress.style.strokeDashoffset = offset;
    }
    
    // Populate dynamic results breakdown
    const detailsContainer = document.getElementById('resultsDetails');
    if (detailsContainer) {
        const allStrengths = [];
        const allImprovements = [];
        state.userAnswers.forEach(ans => {
            if (ans.feedback?.strengths) allStrengths.push(...ans.feedback.strengths);
            if (ans.feedback?.improvements) allImprovements.push(...ans.feedback.improvements);
        });
        
        const topStrengths = Array.from(new Set(allStrengths)).slice(0, 3);
        const topImprovements = Array.from(new Set(allImprovements)).slice(0, 3);
        
        detailsContainer.innerHTML = `
            <div class="results-breakdown-grid">
                <div class="results-metric-card">
                    <div class="rm-value">${(score + 0.3 > 10 ? 9.8 : score + 0.3).toFixed(1)}</div>
                    <div class="rm-label">Technical Depth</div>
                </div>
                <div class="results-metric-card">
                    <div class="rm-value">${(score + 0.5 > 10 ? 9.7 : score + 0.5).toFixed(1)}</div>
                    <div class="rm-label">Communication</div>
                </div>
                <div class="results-metric-card">
                    <div class="rm-value">${state.userAnswers.length} / ${state.totalQuestions}</div>
                    <div class="rm-label">Questions Completed</div>
                </div>
            </div>
            
            <div class="results-feedback-box">
                <h4><i class="fas fa-medal" style="color: var(--primary);"></i> Top Strengths Demonstrated</h4>
                <ul>
                    ${topStrengths.map(s => `<li>${s}</li>`).join('') || '<li>Demonstrated clear structured thinking throughout.</li>'}
                </ul>
            </div>
            
            <div class="results-feedback-box">
                <h4><i class="fas fa-arrow-trend-up" style="color: var(--warning);"></i> Recommended High-Impact Improvements</h4>
                <ul>
                    ${topImprovements.map(i => `<li>${i}</li>`).join('') || '<li>Continue practicing under strict time limits.</li>'}
                </ul>
            </div>
        `;
    }
    
    modal.classList.add('show');
}

function closeModal() {
    const modal = document.getElementById('resultsModal');
    if (modal) modal.classList.remove('show');
}

function resetInterview() {
    state.currentQuestion = 1;
    state.timer = 0;
    state.userAnswers = [];
    state.currentInterview = null;
    
    const setupCard = document.querySelector('.setup-card');
    const interviewScreen = document.getElementById('interviewScreen');
    if (setupCard) setupCard.style.display = 'block';
    if (interviewScreen) interviewScreen.style.display = 'none';
    resetQuestionScreen();
}

function resetQuestionScreen() {
    const answerBox = document.getElementById('answerBox');
    if (answerBox) answerBox.value = '';
    
    const feedbackSection = document.getElementById('feedbackSection');
    if (feedbackSection) feedbackSection.style.display = 'none';
    
    const answerSection = document.querySelector('.answer-section');
    if (answerSection) answerSection.style.display = 'block';
    
    const submitBtn = document.getElementById('submitAnswer');
    if (submitBtn) {
        submitBtn.innerHTML = 'Submit Answer <i class="fas fa-arrow-right"></i>';
        submitBtn.disabled = false;
    }
}

function showHint() {
    const q = state.currentInterview?.currentQuestionData;
    if (q && q.hint) {
        showToast(q.hint, 'info');
        return;
    }
    const hints = [
        "Structure your response with STAR: Situation, Task, Action, Result",
        "Clarify system requirements and performance constraints first",
        "Discuss trade-offs between speed, scalability, and code maintainability",
        "Use concrete metrics and data points from past experience"
    ];
    showToast(hints[Math.floor(Math.random() * hints.length)], 'info');
}

// =================================
// QUESTION LIBRARY POPULATION
// =================================
async function loadQuestionLibrary() {
    const grid = document.getElementById('questionGrid');
    if (!grid) return;
    
    let questions = CURATED_QUESTIONS;
    
    if (state.isLiveApi) {
        try {
            const res = await fetch(`${API_BASE}/api/questions?per_page=50`);
            if (res.ok) {
                const data = await res.json();
                if (data.questions && data.questions.length > 0) {
                    questions = data.questions;
                }
            }
        } catch (e) {
            console.warn('Could not fetch remote questions, using local', e);
        }
    }
    
    renderQuestions(questions);
    
    // Wire up library category filter chips
    const filterContainer = document.getElementById('libraryFilters');
    if (filterContainer) {
        const chips = filterContainer.querySelectorAll('.filter-chip');
        chips.forEach(chip => {
            chip.onclick = function() {
                chips.forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                const cat = this.getAttribute('data-category');
                
                const filtered = (cat === 'all') 
                    ? questions 
                    : questions.filter(q => (q.category || '').toLowerCase() === cat.toLowerCase());
                renderQuestions(filtered);
            };
        });
    }
    
    // Wire up search bar
    const searchInput = document.getElementById('librarySearchInput');
    if (searchInput) {
        searchInput.oninput = debounce(function(e) {
            const query = e.target.value.toLowerCase().trim();
            const filtered = questions.filter(q => 
                (q.text || '').toLowerCase().includes(query) ||
                (q.category || '').toLowerCase().includes(query) ||
                (q.hint || '').toLowerCase().includes(query)
            );
            renderQuestions(filtered);
        }, 250);
    }
}

function renderQuestions(list) {
    const grid = document.getElementById('questionGrid');
    if (!grid) return;
    
    if (!list || list.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-muted);">
                <i class="fas fa-search" style="font-size: 2rem; margin-bottom: 1rem; display: block;"></i>
                No questions found matching your filter criteria.
            </div>
        `;
        return;
    }
    
    grid.innerHTML = list.map(q => `
        <div class="question-card-item">
            <div>
                <div class="q-meta">
                    <span class="category-badge">${(q.category || 'General').toUpperCase()}</span>
                    <span class="difficulty-badge ${q.difficulty || 'medium'}">${(q.difficulty || 'medium').toUpperCase()}</span>
                </div>
                <div class="q-text">${q.text}</div>
                ${q.hint ? `<div class="q-hint"><i class="fas fa-lightbulb" style="color: var(--warning); margin-right: 0.35rem;"></i>${q.hint}</div>` : ''}
            </div>
            <button class="q-action-btn" onclick="practiceSpecificQuestion('${encodeURIComponent(JSON.stringify(q))}')">
                <i class="fas fa-play"></i> Practice This Question
            </button>
        </div>
    `).join('');
}

function practiceSpecificQuestion(encodedQ) {
    try {
        const q = JSON.parse(decodeURIComponent(encodedQ));
        state.selectedLibraryQuestion = q;
        quickStartInterview(q.category || 'technical');
        showToast('Question loaded! Click Start Interview to begin.', 'success');
    } catch (e) {
        console.error('Error queuing question:', e);
    }
}

// =================================
// PAST SESSIONS POPULATION
// =================================
async function loadPastSessions() {
    const grid = document.getElementById('sessionsGrid');
    if (!grid) return;
    
    let sessions = JSON.parse(localStorage.getItem('interviewScores') || '[]');
    
    // Merge with API data if available
    if (state.isLiveApi) {
        try {
            const token = localStorage.getItem('authToken');
            if (token) {
                const res = await fetch(`${API_BASE}/api/interviews?status=completed`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    if (data.interviews && data.interviews.length > 0) {
                        const apiSessions = data.interviews.map(i => ({
                            id: i.id,
                            date: i.startedAt || new Date().toISOString(),
                            score: i.overallScore || 8.0,
                            type: i.type || 'technical',
                            field: i.field || 'software',
                            questionsAnswered: i.questionsAnswered || 5,
                            durationSeconds: i.duration || 600
                        }));
                        // Deduplicate
                        const existingIds = new Set(sessions.map(s => s.id));
                        apiSessions.forEach(as => {
                            if (!existingIds.has(as.id)) sessions.push(as);
                        });
                    }
                }
            }
        } catch (e) {}
    }
    
    // Default demo session if completely empty
    if (sessions.length === 0) {
        sessions = [
            {
                id: 'demo-1',
                date: new Date(Date.now() - 3600000 * 2).toISOString(),
                score: 9.2,
                type: 'technical',
                field: 'software',
                questionsAnswered: 5,
                durationSeconds: 940
            },
            {
                id: 'demo-2',
                date: new Date(Date.now() - 86400000 * 2).toISOString(),
                score: 8.5,
                type: 'behavioral',
                field: 'software',
                questionsAnswered: 4,
                durationSeconds: 780
            },
            {
                id: 'demo-3',
                date: new Date(Date.now() - 86400000 * 4).toISOString(),
                score: 7.8,
                type: 'system-design',
                field: 'software',
                questionsAnswered: 3,
                durationSeconds: 1200
            }
        ];
        localStorage.setItem('interviewScores', JSON.stringify(sessions));
    }
    
    renderSessions(sessions);
    
    // Wire filter dropdowns
    const typeFilter = document.getElementById('sessionTypeFilter');
    const timeFilter = document.getElementById('sessionTimeFilter');
    
    function applyFilters() {
        const typeVal = typeFilter ? typeFilter.value : 'all';
        const timeVal = timeFilter ? timeFilter.value : 'all';
        
        let filtered = sessions;
        if (typeVal !== 'all') {
            filtered = filtered.filter(s => (s.type || '').toLowerCase() === typeVal.toLowerCase());
        }
        if (timeVal !== 'all') {
            const cutoffDays = parseInt(timeVal);
            const cutoffMs = Date.now() - (cutoffDays * 86400000);
            filtered = filtered.filter(s => new Date(s.date).getTime() >= cutoffMs);
        }
        renderSessions(filtered);
    }
    
    if (typeFilter) typeFilter.onchange = applyFilters;
    if (timeFilter) timeFilter.onchange = applyFilters;
}

function renderSessions(list) {
    const grid = document.getElementById('sessionsGrid');
    if (!grid) return;
    
    if (!list || list.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-muted);">
                <i class="fas fa-history" style="font-size: 2rem; margin-bottom: 1rem; display: block;"></i>
                No interview sessions recorded yet. Start practicing now!
            </div>
        `;
        return;
    }
    
    grid.innerHTML = list.map(s => {
        const score = parseFloat(s.score || 0);
        const scoreClass = score >= 8.5 ? 'high' : (score >= 7.0 ? 'mid' : 'low');
        const formattedDate = new Date(s.date).toLocaleDateString('en-US', {
            month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
        });
        const durationMin = Math.round((s.durationSeconds || 600) / 60);
        
        return `
            <div class="session-card">
                <div>
                    <div class="sc-header">
                        <span class="category-badge">${(s.type || 'Technical').toUpperCase()}</span>
                        <span class="sc-score-badge ${scoreClass}">${score.toFixed(1)} / 10</span>
                    </div>
                    <div class="sc-title">${(s.field || 'Software Engineering').toUpperCase()} Round</div>
                    <div class="sc-info">
                        <span><i class="far fa-calendar-alt"></i> ${formattedDate}</span>
                        <span><i class="far fa-clock"></i> ${durationMin} mins</span>
                        <span><i class="fas fa-tasks"></i> ${s.questionsAnswered || 5} questions</span>
                    </div>
                </div>
                <button class="sc-details-btn" onclick="reviewSessionReport('${encodeURIComponent(JSON.stringify(s))}')">
                    <i class="fas fa-chart-pie"></i> View Session Feedback
                </button>
            </div>
        `;
    }).join('');
}

function reviewSessionReport(encodedS) {
    try {
        const s = JSON.parse(decodeURIComponent(encodedS));
        showResultsModal(s.score);
    } catch (e) {
        console.error('Session modal error:', e);
    }
}

// =================================
// OVERVIEW STATS SYNCHRONIZATION
// =================================
function loadOverviewStats() {
    const sessions = JSON.parse(localStorage.getItem('interviewScores') || '[]');
    const completedCount = sessions.length || 24;
    
    const validScores = sessions.filter(s => s.score).map(s => s.score);
    const avg = validScores.length 
        ? (validScores.reduce((a, b) => a + b, 0) / validScores.length).toFixed(1)
        : '8.5';
        
    const totalSec = sessions.reduce((sum, s) => sum + (s.durationSeconds || 900), 0) || 45000;
    const hours = Math.floor(totalSec / 3600);
    const mins = Math.floor((totalSec % 3600) / 60);
    
    // Update overview DOM stat cards if present
    const completedEl = document.querySelector('.stat-card.blue h3');
    if (completedEl) completedEl.textContent = completedCount;
    
    const avgScoreEl = document.querySelector('.stat-card.green h3');
    if (avgScoreEl) avgScoreEl.textContent = `${avg}/10`;
    
    const timeEl = document.querySelector('.stat-card.purple h3');
    if (timeEl) timeEl.textContent = `${hours}h ${mins}m`;
    
    const streakEl = document.querySelector('.stat-card.orange h3');
    if (streakEl) streakEl.textContent = '7 Days';
}

// =================================
// CHART.JS VISUALIZATIONS
// =================================
function initCharts() {
    if (typeof Chart === 'undefined') return;
    
    // Clean modern theme options
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Inter', sans-serif";
    
    // 1. Performance Trend Area Chart
    const perfCanvas = document.getElementById('performanceChart');
    if (perfCanvas) {
        if (state.charts.perf) state.charts.perf.destroy();
        const ctx = perfCanvas.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(56, 189, 248, 0.4)');
        gradient.addColorStop(1, 'rgba(56, 189, 248, 0.0)');
        
        state.charts.perf = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Day 1', 'Day 3', 'Day 7', 'Day 12', 'Day 18', 'Day 24', 'Today'],
                datasets: [{
                    label: 'Overall Score (0-10)',
                    data: [7.2, 7.6, 8.0, 8.2, 8.7, 9.0, 9.2],
                    borderColor: '#38bdf8',
                    backgroundColor: gradient,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#38bdf8',
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 5, max: 10, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                    x: { grid: { display: false } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
    
    // 2. Score Distribution Bar Chart
    const scoreCanvas = document.getElementById('scoreChart');
    if (scoreCanvas) {
        if (state.charts.score) state.charts.score.destroy();
        state.charts.score = new Chart(scoreCanvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['5-6', '6-7', '7-8', '8-9', '9-10'],
                datasets: [{
                    label: 'Answers',
                    data: [1, 3, 8, 14, 9],
                    backgroundColor: 'rgba(56, 189, 248, 0.7)',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
    
    // 3. Interview Types Doughnut Chart
    const typeCanvas = document.getElementById('typeChart');
    if (typeCanvas) {
        if (state.charts.type) state.charts.type.destroy();
        state.charts.type = new Chart(typeCanvas.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Technical', 'Behavioral', 'System Design', 'HR'],
                datasets: [{
                    data: [14, 8, 5, 3],
                    backgroundColor: ['#38bdf8', '#8b5cf6', '#10b981', '#f59e0b'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 12, padding: 15 } }
                }
            }
        });
    }
    
    // 4. Skills Assessment Radar Chart
    const skillsCanvas = document.getElementById('skillsChart');
    if (skillsCanvas) {
        if (state.charts.skills) state.charts.skills.destroy();
        state.charts.skills = new Chart(skillsCanvas.getContext('2d'), {
            type: 'radar',
            data: {
                labels: ['Technical Accuracy', 'Communication', 'Architecture', 'STAR Structure', 'Depth'],
                datasets: [{
                    label: 'Candidate Competency',
                    data: [8.8, 9.2, 7.8, 8.5, 8.2],
                    backgroundColor: 'rgba(139, 92, 246, 0.25)',
                    borderColor: '#8b5cf6',
                    pointBackgroundColor: '#8b5cf6'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                        grid: { color: 'rgba(255, 255, 255, 0.08)' },
                        suggestedMin: 5,
                        suggestedMax: 10,
                        ticks: { display: false }
                    }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
    
    // 5. Time Analysis Bar Chart
    const timeCanvas = document.getElementById('timeChart');
    if (timeCanvas) {
        if (state.charts.time) state.charts.time.destroy();
        state.charts.time = new Chart(timeCanvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Minutes Practiced',
                    data: [25, 45, 30, 60, 20, 50, 75],
                    backgroundColor: 'rgba(16, 185, 129, 0.7)',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
}

// =================================
// TOAST NOTIFICATIONS
// =================================
function showToast(message, type = 'success') {
    let toast = document.getElementById('toast');
    let toastMessage = document.getElementById('toastMessage');
    
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        toast.innerHTML = `<i class="fas fa-check-circle"></i><span id="toastMessage"></span>`;
        document.body.appendChild(toast);
        toastMessage = document.getElementById('toastMessage');
    }
    
    if (toast && toastMessage) {
        toastMessage.textContent = message;
        toast.className = `toast show ${type}`;
        const icon = toast.querySelector('i');
        if (icon) {
            icon.className = type === 'success' ? 'fas fa-check-circle' :
                           type === 'error' ? 'fas fa-exclamation-circle' :
                           'fas fa-info-circle';
        }
        setTimeout(() => toast.classList.remove('show'), 3500);
    }
}

// =================================
// SETTINGS FUNCTIONALITY
// =================================
document.querySelectorAll('.settings-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const nameInput = this.querySelector('input[type="text"]');
        const emailInput = this.querySelector('input[type="email"]');
        if (nameInput) {
            const parts = nameInput.value.split(' ');
            const userData = JSON.parse(localStorage.getItem('userData') || '{}');
            userData.firstName = parts[0] || 'User';
            userData.lastName = parts.slice(1).join(' ') || '';
            if (emailInput) userData.email = emailInput.value;
            localStorage.setItem('userData', JSON.stringify(userData));
            loadUserData();
        }
        showToast('Settings saved successfully!', 'success');
    });
});

// =================================
// UTILITIES & SHORTCUTS
// =================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-bar input');
        if (searchInput) searchInput.focus();
    }
    if (e.key === 'Escape') {
        closeModal();
        closeVideo();
        const dropdown = document.getElementById('userDropdown');
        if (dropdown) dropdown.classList.remove('show');
    }
});

// =================================
// GLOBAL WINDOW EXPORTS
// =================================
window.playVideo = playVideo;
window.closeVideo = closeVideo;
window.logout = logout;
window.startNewInterview = startNewInterview;
window.quickStartInterview = quickStartInterview;
window.startInterview = startInterview;
window.submitAnswer = submitAnswer;
window.nextQuestion = nextQuestion;
window.skipQuestion = skipQuestion;
window.endInterview = endInterview;
window.closeModal = closeModal;
window.showHint = showHint;
window.showPage = showPage;
window.practiceSpecificQuestion = practiceSpecificQuestion;
window.reviewSessionReport = reviewSessionReport;

console.log('✅ AI Interview Coach Master Script loaded successfully');
