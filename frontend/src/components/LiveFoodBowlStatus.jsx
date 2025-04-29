import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Bell, PawPrint } from "lucide-react";

const LiveFoodBowlStatus = () => {
  // Sample data
  const foodWeightGrams = 150;
  const foodCapacityGrams = 500;
  const foodPercentage = (foodWeightGrams / foodCapacityGrams) * 100;
  const isPetNearby = true;
  const isLowFood = foodPercentage < 20;
  
  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <CardTitle>Live Food Bowl Status</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Food Weight */}
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-sm text-gray-500">Current Food Level</span>
            <span className="text-sm font-medium">{foodWeightGrams}g / {foodCapacityGrams}g</span>
          </div>
          <Progress value={foodPercentage} className="h-2" />
        </div>
        
        {/* Alerts */}
        <div className="space-y-4">
          {/* Low Food Alert */}
          {isLowFood && (
            <div className="flex items-center p-3 bg-tummy-red-light rounded-lg animate-pulse-slow">
              <Bell size={18} className="text-tummy-red-dark mr-2" />
              <span className="text-sm font-medium text-tummy-red-dark">Low Food Alert!</span>
            </div>
          )}
          
          {/* Pet Detection */}
          <div className="flex items-center justify-between border rounded-lg p-3">
            <div className="flex items-center">
              <PawPrint size={18} className="mr-2 text-gray-500" />
              <span className="text-sm">Pet Near Bowl</span>
            </div>
            <div>
              {isPetNearby ? (
                <div className="flex items-center">
                  <span className="text-sm font-medium text-tummy-green-dark mr-2">Yes</span>
                  <div className="relative">
                    <div className="absolute -inset-1 rounded-full bg-tummy-green animate-pulse opacity-40"></div>
                    <div className="relative w-3 h-3 bg-tummy-green-dark rounded-full"></div>
                  </div>
                </div>
              ) : (
                <div className="flex items-center">
                  <span className="text-sm font-medium text-gray-400 mr-2">No</span>
                  <div className="w-3 h-3 bg-gray-300 rounded-full"></div>
                </div>
              )}
            </div>
          </div>

          {/* Pet Animation */}
          {isPetNearby && (
            <div className="flex justify-center pt-2">
              <div className="animate-bounce-in">
                {/* Cute Pet SVG Animation */}
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M32 14C32 10.6863 34.6863 8 38 8C41.3137 8 44 10.6863 44 14C44 17.3137 41.3137 20 38 20C34.6863 20 32 17.3137 32 14Z" fill="#CFDEF3"/>
                  <path d="M4 14C4 10.6863 6.68629 8 10 8C13.3137 8 16 10.6863 16 14C16 17.3137 13.3137 20 10 20C6.68629 20 4 17.3137 4 14Z" fill="#CFDEF3"/>
                  <path d="M25 38C32.1797 38 38 32.1797 38 25C38 17.8203 32.1797 12 25 12C17.8203 12 12 17.8203 12 25C12 32.1797 17.8203 38 25 38Z" fill="#CFDEF3"/>
                  <path d="M18 26C19.1046 26 20 25.1046 20 24C20 22.8954 19.1046 22 18 22C16.8954 22 16 22.8954 16 24C16 25.1046 16.8954 26 18 26Z" fill="#333"/>
                  <path d="M32 26C33.1046 26 34 25.1046 34 24C34 22.8954 33.1046 22 32 22C30.8954 22 30 22.8954 30 24C30 25.1046 30.8954 26 32 26Z" fill="#333"/>
                  <path d="M25 32C26.1046 32 27 31.1046 27 30C27 28.8954 26.1046 28 25 28C23.8954 28 23 28.8954 23 30C23 31.1046 23.8954 32 25 32Z" fill="#333"/>
                  <path d="M25 40C19.4772 40 15 41.7909 15 44C15 46.2091 19.4772 48 25 48C30.5228 48 35 46.2091 35 44C35 41.7909 30.5228 40 25 40Z" fill="#B2DFDB"/>
                </svg>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default LiveFoodBowlStatus;
