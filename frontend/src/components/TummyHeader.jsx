import React from 'react';

const TummyHeader = () => {

  return (
    <header className="w-full py-4 px-6 bg-white border-b border-gray-200 flex justify-between items-center">
      <div className="flex items-center">
        <div className="text-primary font-bold text-2xl flex items-center gap-2">
          <img
            src="/tummytimer.svg"
            alt="Tummy Timer Logo"
            className="h-8 w-8"
          />
          TummyTimer
        </div>
      </div>
    </header>
  );
};

export default TummyHeader;
