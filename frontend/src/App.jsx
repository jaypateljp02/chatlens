import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';

import ChatUpload from './components/Upload/ChatUpload';
import DashboardOverview from './components/Dashboard/DashboardOverview';
import SummariesPage from './components/Summaries/SummariesPage';
import AnalyticsDashboard from './components/Analytics/AnalyticsDashboard';
import SentimentDashboard from './components/Sentiment/SentimentDashboard';
import PeoplePage from './components/People/PeoplePage';
import ActionTracker from './components/Actions/ActionTracker';
import TimelineView from './components/Timeline/TimelineView';
import TopicExtraction from './components/Topics/TopicExtraction';
import KnowledgeGraphView from './components/KnowledgeGraph/KnowledgeGraphView';
import SettingsPage from './components/Settings/SettingsPage';

const App = () => {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<ChatUpload />} />
          <Route path="/dashboard" element={<DashboardOverview />} />
          <Route path="/summaries" element={<SummariesPage />} />
          <Route path="/analytics" element={<AnalyticsDashboard />} />
          <Route path="/sentiment" element={<SentimentDashboard />} />
          <Route path="/people" element={<PeoplePage />} />
          <Route path="/topics" element={<TopicExtraction />} />
          <Route path="/timeline" element={<TimelineView />} />
          <Route path="/actions" element={<ActionTracker />} />
          <Route path="/knowledge-graph" element={<KnowledgeGraphView />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};

export default App;
