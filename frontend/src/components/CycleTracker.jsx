import React from 'react';

function CycleTracker({ cycleData }) {
  if (!cycleData) return null;

  const usedPercent = (cycleData.after_trip / 70) * 100;
  const remainingPercent = (cycleData.remaining / 70) * 100;

  return (
    <div>
      <h3 className="font-semibold text-[#1d1d1f] mb-3">70-Hour Cycle Tracking</h3>
      
      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>Used: {cycleData.after_trip?.toFixed(1) || 0} hrs</span>
          <span>Remaining: {cycleData.remaining?.toFixed(1) || 0} hrs</span>
        </div>
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-[#007aff] rounded-full transition-all duration-500"
            style={{ width: `${Math.min(usedPercent, 100)}%` }}
          />
        </div>
        <div className="text-right text-xs text-gray-400 mt-1">Limit: 70 hours / 8 days</div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-3 gap-3 mt-4">
        <div className="text-center p-2 bg-gray-50 rounded-lg">
          <div className="text-xs text-gray-500">Started With</div>
          <div className="text-lg font-semibold text-[#1d1d1f]">{cycleData.started_with?.toFixed(1) || 0}h</div>
        </div>
        <div className="text-center p-2 bg-gray-50 rounded-lg">
          <div className="text-xs text-gray-500">Trip Added</div>
          <div className="text-lg font-semibold text-[#febc2e]">+{cycleData.trip_added?.toFixed(1) || 0}h</div>
        </div>
        <div className="text-center p-2 bg-gray-50 rounded-lg">
          <div className="text-xs text-gray-500">Remaining</div>
          <div className="text-lg font-semibold text-[#28c840]">{cycleData.remaining?.toFixed(1) || 0}h</div>
        </div>
      </div>
    </div>
  );
}

export default CycleTracker;
