import React from 'react';
import TummyHeader from '@/components/TummyHeader';
import FeedingHistoryTable from '@/components/FeedingHistoryTable';
import TodayFeedingStatus from '@/components/TodayFeedingStatus';
import FutureFeedingPredictions from '@/components/FutureFeedingPredictions';
import LiveFoodBowlStatus from '@/components/LiveFoodBowlStatus';

const Index = () => {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <TummyHeader />
      
      <main className="flex-1 p-6">
        <div className="max-w-7xl mx-auto space-y-6">
          <h1 className="text-2xl font-bold text-gray-800">TummyTimer Dashboard</h1>
          
          {/* Top Row - Status Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="col-span-1">
              <TodayFeedingStatus />
            </div>
            <div className="col-span-1 md:col-span-2">
              <LiveFoodBowlStatus />
            </div>
          </div>
          
          {/* Bottom Row - Tables */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="col-span-1">
              <FeedingHistoryTable />
            </div>
            <div className="col-span-1">
              <FutureFeedingPredictions />
            </div>
          </div>
        </div>
      </main>

      <footer className="py-4 px-6 border-t border-gray-200 text-center text-sm text-gray-500">
        © {new Date().getFullYear()} TummyTimer • Keep your pets well fed and happy
      </footer>
    </div>
  );
};

export default Index;
