import React, { useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import LandingPage from './components/LandingPage';
import AuthPage from './components/AuthPage';
import PlansPage from './components/PlansPage';
import ConnectChannel from './components/ConnectChannel';
import Dashboard from './components/Dashboard';
import ClipsReview from './components/ClipsReview';
import SocialConnect from './components/SocialConnect';
import SuccessPage from './components/SuccessPage';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';
const STORAGE_KEY = 'zebec-ai-app-state-v1';
const PAGE_GUARDS = {
  plans: ['userData'],
  'connect-channel': ['selectedPlan'],
  dashboard: ['linkedChannels'],
  'clips-review': ['clips'],
  'social-connect': ['clips'],
  success: ['clips', 'connectedPlatforms'],
};

const defaultState = {
  currentPage: 'landing',
  userData: null,
  selectedPlan: null,
  linkedChannels: [],
  clips: [],
  connectedPlatforms: [],
};

const PLAN_BY_ID = {
  starter: { id: 'starter', name: 'Starter', monthlyPrice: 0, monthlyClipLimit: 20, recommended: false },
  growth: { id: 'growth', name: 'Growth', monthlyPrice: 19, monthlyClipLimit: 120, recommended: true },
  scale: { id: 'scale', name: 'Scale', monthlyPrice: 49, monthlyClipLimit: 500, recommended: false },
};

async function apiRequest(endpoint, method = 'GET', body = null) {
  const token = localStorage.getItem('zebec-token');
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (token) {
    options.headers.Authorization = `Bearer ${token}`;
  }

  if (body !== null) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(payload.message || 'Request failed.');
  }

  return payload;
}

function getStoredState() {
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) return defaultState;
  try {
    const parsed = JSON.parse(raw);
    return {
      ...defaultState,
      ...parsed,
      linkedChannels: Array.isArray(parsed.linkedChannels) ? parsed.linkedChannels : [],
      clips: Array.isArray(parsed.clips) ? parsed.clips : [],
      connectedPlatforms: Array.isArray(parsed.connectedPlatforms) ? parsed.connectedPlatforms : [],
    };
  } catch (error) {
    console.error('Could not parse saved state. Starting fresh.', error);
    return defaultState;
  }
}

function ensureGuardedPage(page, nextState) {
  const requirements = PAGE_GUARDS[page];
  if (!requirements) return page;
  for (const requirement of requirements) {
    if (requirement === 'userData' && !nextState.userData) return 'auth';
    if (requirement === 'selectedPlan' && !nextState.selectedPlan) return 'plans';
    if (requirement === 'linkedChannels' && nextState.linkedChannels.length === 0) return 'connect-channel';
    if (requirement === 'clips' && nextState.clips.length === 0) return 'dashboard';
    if (requirement === 'connectedPlatforms' && nextState.connectedPlatforms.length === 0) return 'social-connect';
  }
  return page;
}

export default function App() {
  const [appState, setAppState] = useState(getStoredState);
  const { currentPage, userData, selectedPlan, linkedChannels, clips, connectedPlatforms } = appState;

  const updateState = (updater) => {
    setAppState((previousState) => {
      const nextState = typeof updater === 'function' ? updater(previousState) : { ...previousState, ...updater };
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextState));
      return nextState;
    });
  };

  const navigate = (page) => {
    updateState((previousState) => ({
      ...previousState,
      currentPage: ensureGuardedPage(page, previousState),
    }));
  };

  useEffect(() => {
    const restoreSession = async () => {
      const token = window.localStorage.getItem('zebec-token');
      if (!token) return;

      try {
        const me = await apiRequest('/me');
        const plansResponse = await apiRequest('/plans');
        const channelsResponse = await apiRequest('/channels');
        const clipsResponse = await apiRequest('/clips');

        const selectedPlan = plansResponse.plans.find((plan) => plan.id === me.user.selectedPlan) || null;
        const linkedChannels = channelsResponse.channels.map((channel) => ({
          id: channel.id,
          platform: channel.platform,
          name: channel.handle,
          subscribers: channel.subscriber_count,
          videos: channel.platform === 'youtube' ? 342 : 156,
          totalViews: channel.platform === 'youtube' ? '12.5M' : '8.3M',
        }));
        const clipsData = clipsResponse.clips.map((clip) => ({
          id: clip.id,
          title: clip.title,
          durationSeconds: clip.duration_seconds,
          hook: clip.hook,
          script: clip.script,
          approved: Boolean(clip.approved),
          createdAt: clip.created_at,
        }));

        updateState((previousState) => ({
          ...previousState,
          userData: {
            id: me.user.id,
            email: me.user.email,
            name: me.user.name,
          },
          selectedPlan: selectedPlan
            ? {
                id: selectedPlan.id,
                name: selectedPlan.name,
                monthlyPrice: selectedPlan.price,
                monthlyClipLimit: selectedPlan.clip_limit,
                recommended: Boolean(selectedPlan.recommended),
              }
            : previousState.selectedPlan,
          linkedChannels,
          clips: clipsData,
          currentPage: previousState.currentPage === 'landing' ? 'dashboard' : previousState.currentPage,
        }));
      } catch (error) {
        window.localStorage.removeItem('zebec-token');
      }
    };

    restoreSession();
  }, []);

  const handleLogin = async ({ email, name, password }) => {
    try {
      const registerResult = await apiRequest('/auth/register', 'POST', { name, email, password });
      localStorage.setItem('zebec-token', registerResult.token);
      const nextUser = {
        id: registerResult.user.id,
        email: registerResult.user.email,
        name: registerResult.user.name,
      };
      updateState((previousState) => ({
        ...previousState,
        userData: nextUser,
        currentPage: 'plans',
      }));
      return { ok: true };
    } catch (registerError) {
      try {
        const loginResult = await apiRequest('/auth/login', 'POST', { email, password });
        localStorage.setItem('zebec-token', loginResult.token);
        const nextUser = {
          id: loginResult.user.id,
          email: loginResult.user.email,
          name: loginResult.user.name,
        };
        updateState((previousState) => ({
          ...previousState,
          userData: nextUser,
          currentPage: 'plans',
        }));
        return { ok: true };
      } catch (loginError) {
        return { ok: false, message: loginError.message };
      }
    }
  };

  const handlePlanSelect = async (plan) => {
    try {
      const mappedPlan = PLAN_BY_ID[plan] || PLAN_BY_ID.starter;
      await apiRequest('/plans/select', 'POST', { planId: mappedPlan.id });
      updateState((previousState) => ({
        ...previousState,
        selectedPlan: mappedPlan,
        currentPage: 'connect-channel',
      }));
      return { ok: true };
    } catch (error) {
      return { ok: false, message: error.message };
    }
  };

  const handleChannelLink = async ({ platform, handle, subscribers }) => {
    try {
      const channelResponse = await apiRequest('/channels', 'POST', {
        platform,
        handle,
        subscriberCount: subscribers,
      });
      const channel = {
        id: channelResponse.channel.id,
        platform: channelResponse.channel.platform,
        name: channelResponse.channel.handle,
        subscribers: channelResponse.channel.subscriber_count,
        videos: platform === 'youtube' ? 342 : 156,
        totalViews: platform === 'youtube' ? '12.5M' : '8.3M',
      };
      updateState((previousState) => ({
        ...previousState,
        linkedChannels: previousState.linkedChannels.some(
          (existingChannel) => existingChannel.platform === channel.platform && existingChannel.name === channel.name
        )
          ? previousState.linkedChannels
          : [...previousState.linkedChannels, channel],
        currentPage: 'dashboard',
      }));
      return { ok: true };
    } catch (error) {
      return { ok: false, message: error.message };
    }
  };

  const handleClipsGenerated = async ({ topic }) => {
    try {
      const response = await apiRequest('/clips/generate', 'POST', { topic });
      const newClips = response.clips.map((clip) => ({
        id: clip.id,
        title: clip.title,
        durationSeconds: clip.duration_seconds,
        hook: clip.hook,
        script: clip.script,
        approved: Boolean(clip.approved),
        createdAt: clip.created_at,
      }));
      updateState((previousState) => ({
        ...previousState,
        clips: newClips,
        currentPage: 'clips-review',
      }));
      return { ok: true };
    } catch (error) {
      return { ok: false, message: error.message };
    }
  };

  const handlePlatformConnect = (platform) => {
    updateState((previousState) => ({
      ...previousState,
      connectedPlatforms: previousState.connectedPlatforms.includes(platform)
        ? previousState.connectedPlatforms
        : [...previousState.connectedPlatforms, platform],
    }));
  };

  const handleClipApprovalToggle = (clipId) => {
    updateState((previousState) => ({
      ...previousState,
      clips: previousState.clips.map((clip) =>
        clip.id === clipId ? { ...clip, approved: !clip.approved } : clip
      ),
    }));
  };

  const handlePublish = async () => {
    try {
      await apiRequest('/publish', 'POST', {
        platforms: connectedPlatforms.length > 0 ? connectedPlatforms : ['youtube'],
      });
      updateState((previousState) => ({
        ...previousState,
        currentPage: ensureGuardedPage('success', previousState),
      }));
      return { ok: true };
    } catch (error) {
      return { ok: false, message: error.message };
    }
  };

  const handleReset = () => {
    window.localStorage.removeItem(STORAGE_KEY);
    window.localStorage.removeItem('zebec-token');
    setAppState(defaultState);
  };

  const approvedClipCount = clips.filter((clip) => clip.approved).length;

  const sharedProps = {
    navigate,
    userData,
    selectedPlan,
    linkedChannels,
    clips,
    connectedPlatforms,
    approvedClipCount,
    handleLogin,
    handlePlanSelect,
    handleChannelLink,
    handleClipsGenerated,
    handlePlatformConnect,
    handleClipApprovalToggle,
    handlePublish,
    handleReset,
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'landing': return <LandingPage {...sharedProps} />;
      case 'auth': return <AuthPage {...sharedProps} />;
      case 'plans': return <PlansPage {...sharedProps} />;
      case 'connect-channel': return <ConnectChannel {...sharedProps} />;
      case 'dashboard': return <Dashboard {...sharedProps} />;
      case 'clips-review': return <ClipsReview {...sharedProps} />;
      case 'social-connect': return <SocialConnect {...sharedProps} />;
      case 'success': return <SuccessPage {...sharedProps} />;
      default: return <LandingPage {...sharedProps} />;
    }
  };

  return (
    <div className="app-shell">
      <Navbar navigate={navigate} userData={userData} currentPage={currentPage} />
      {renderPage()}
    </div>
  );
}