import React, { useState, useEffect } from 'react';
import DashboardPage from '@/components/pages/DashboardPage';
import Icon from '@/components/atoms/Icon';

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/data.json')
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load data", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center text-primary gap-4">
        <div className="w-10 h-10 rounded-full bg-primary-container flex items-center justify-center">
          <Icon name="insights" className="text-on-primary-container" filled />
        </div>
        <p className="font-label-sm tracking-wider uppercase">Loading Pulse Engine...</p>
      </div>
    );
  }

  return <DashboardPage data={data} />;
}
