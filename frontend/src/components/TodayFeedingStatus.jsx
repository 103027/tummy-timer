import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Clock } from "lucide-react";

const TodayFeedingStatus = () => {
  // Sample data
  const isFedToday = true;
  const lastFeedingTime = "12:30 PM";
  const lastFeedingAmount = 30;
  
  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <CardTitle>Today's Feeding Status</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Fed Today or Not */}
          <div className="flex items-center space-x-2">
            <div className={`w-4 h-4 rounded-full ${isFedToday ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="font-medium">{isFedToday ? 'Fed Today' : 'Not Fed Today'}</span>
          </div>
          
          {/* Last Feeding Info */}
          <div className="pt-2 border-t border-gray-100">
            <div className="flex items-start">
              <div className="bg-tummy-blue-light p-2 rounded-lg mr-3">
                <Clock size={20} className="text-primary" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Last Feeding</p>
                <p className="font-medium">
                  {lastFeedingTime} • {lastFeedingAmount}g
                </p>
              </div>
            </div>
          </div>

          {/* Feed Now Button */}
          <button className="feed-now-btn w-full">
            Feed Now
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

export default TodayFeedingStatus;
