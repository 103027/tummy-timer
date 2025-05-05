import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Clock } from "lucide-react";

const TodayFeedingStatus = () => {
  const [isFedToday, setIsFedToday] = useState(false);

  useEffect(() => {
    axios.get("http://127.0.0.1:5001/status/today")
      .then((res) => {
          setIsFedToday(res.data.fed_today);
      })
      .catch((err) => {
        console.error("Error fetching feeding status:", err);
      });
  }, []);

  const handleFeedNow = () => {
    axios.post("http://127.0.0.1:5001/control/feed-now")
      .then(() => alert("Feed Now command sent successfully"))
      .catch((err) => {
        console.error("Failed to send Feed Now command:", err);
        alert("Failed to send Feed Now command");
      });
  };

  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <CardTitle>Feeding Status</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Fed Today or Not */}
          <div className="flex items-center space-x-2">
            <div className={`w-4 h-4 rounded-full ${isFedToday ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="font-medium">{isFedToday ? 'Fed Today' : 'Not Fed Today'}</span>
          </div>

          {/* Last Feeding Info */}
          {/* {lastFeedingTime && (
            <div className="pt-2 border-t border-gray-100">
              <div className="flex items-start">
                <div className="bg-tummy-blue-light p-2 rounded-lg mr-3">
                  <Clock size={20} className="text-primary" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Last Feeding</p>
                  <p className="font-medium">{lastFeedingTime}</p>
                </div>
              </div>
            </div>
          )} */}

          {/* Feed Now Button */}
          <button onClick={handleFeedNow} className="feed-now-btn w-full">
            Feed Now
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

export default TodayFeedingStatus;
