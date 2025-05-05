import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Bell, PawPrint } from "lucide-react";

const LiveFoodBowlStatus = () => {
  const [sensorData, setSensorData] = useState(null);
  const [totalPortionsToday, setTotalPortionsToday] = useState(1);

  useEffect(() => {
    // Fetch sensor data
    axios.get("http://127.0.0.1:5001/sensor/portions")
      .then((res) => setSensorData(res.data))
      .catch((err) => console.error("Failed to fetch sensor data:", err));

    // Fetch schedules
    axios.get("http://127.0.0.1:5001/schedule")
      .then((res) => {
        const today = new Date().toLocaleString('en-US', { weekday: 'short' }); // e.g., "Thu"
        const schedulesToday = res.data.filter(sch => sch.days.includes(today));
        const total = schedulesToday.reduce((sum, sch) => sum + (sch.portion || 0), 0);
        setTotalPortionsToday(total || 1); // default to 1 if none scheduled
      })
      .catch((err) => console.error("Failed to fetch schedules:", err));
  }, []);

  if (!sensorData) return <p>Loading...</p>;

  const foodWeightGrams = sensorData.total_weight_today;
  console.log(foodWeightGrams);
  const today_portion = foodWeightGrams/ 25;
  const foodPercentage = (today_portion / totalPortionsToday) * 100;

  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <CardTitle>Today's Food Bowl Status</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Food Weight */}
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-sm text-gray-500">Current Food Level</span>
            <span className="text-sm font-medium">{today_portion} / {totalPortionsToday} portions</span>
          </div>
          <Progress value={foodPercentage} className="h-2" />
        </div>
      </CardContent>
    </Card>
  );
};

export default LiveFoodBowlStatus;
