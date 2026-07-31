import React from 'react';
import SmartSummary from './SmartSummary';
import AskQuestion from './AskQuestion';
import './Summaries.css';

const SummariesPage = () => {
  return (
    <div className="summaries-container">
      <SmartSummary />
      <AskQuestion />
    </div>
  );
};

export default SummariesPage;
