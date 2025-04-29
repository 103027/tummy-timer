import React from 'react';
import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";

const TummyHeader = () => {
  const handleLogout = () => {
    console.log("Logging out...");
    // Add actual logout functionality here (e.g., clear localStorage and redirect)
  };
  
  return (
    <header className="w-full py-4 px-6 bg-white border-b border-gray-200 flex justify-between items-center">
      <div className="flex items-center">
        <div className="text-primary font-bold text-2xl flex items-center gap-2">
          {/* TummyTimer Logo SVG */}
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#B2DFDB" />
            <path d="M10 16C10 15.4477 10.4477 15 11 15H21C21.5523 15 22 15.4477 22 16V22C22 23.6569 20.6569 25 19 25H13C11.3431 25 10 23.6569 10 22V16Z" fill="white" />
            <path d="M11 10C11 9.44772 11.4477 9 12 9H20C20.5523 9 21 9.44772 21 10V15H11V10Z" fill="white" />
            <path d="M14 12H18" stroke="#B2DFDB" strokeWidth="1.5" strokeLinecap="round" />
            <path d="M14 19H18" stroke="#B2DFDB" strokeWidth="1.5" strokeLinecap="round" />
          </svg>
          TummyTimer
        </div>
      </div>

      <Button variant="ghost" onClick={handleLogout} className="flex items-center gap-2">
        <LogOut size={18} />
        <span>Logout</span>
      </Button>
    </header>
  );
};

export default TummyHeader;
