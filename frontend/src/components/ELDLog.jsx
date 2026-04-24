import React from 'react';

function ELDLog({ dayNumber, date, drivingHours, onDutyHours, totalMiles, logEntries }) {
  const formatDate = (dateStr) => {
    if (!dateStr) return '______';
    const d = new Date(dateStr);
    return `${d.getMonth()+1}/${d.getDate()}/${d.getFullYear()}`;
  };

  return (
    <div className="border border-gray-200 rounded-xl overflow-hidden bg-white">
      {/* Log Header */}
      <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <h3 className="font-semibold text-[#1d1d1f]">Day {dayNumber} Log</h3>
          <div className="text-sm text-gray-500">
            Date: {formatDate(date)} | Miles: {totalMiles || 0} | Drive: {drivingHours || 0}h | On-Duty: {onDutyHours || 0}h
          </div>
        </div>
      </div>

      {/* Log Grid - Placeholder */}
      <div className="p-4">
        <div className="bg-gray-100 rounded-lg p-8 text-center text-gray-500">
          📋 ELD Log Grid Coming Soon
          <div className="text-xs mt-2">
            {logEntries && logEntries.length > 0 ? `${logEntries.length} log entries` : 'No log entries yet'}
          </div>
        </div>
        
        {/* Preview log entries if they exist */}
        {logEntries && logEntries.length > 0 && (
          <div className="mt-3 text-xs text-gray-400">
            {logEntries.map((entry, idx) => (
              <span key={idx} className="inline-block mr-2">
                {entry.start}-{entry.end}: {entry.status}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ELDLog;
