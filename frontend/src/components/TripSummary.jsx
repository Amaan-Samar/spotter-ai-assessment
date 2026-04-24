import React from 'react';

function TripSummary({ tripData }) {
  return (
    <div>
      <h3 className="font-semibold text-[#1d1d1f] mb-3">Trip Summary</h3>
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-500">Total Distance:</span>
          <span className="font-medium">{tripData.total_miles?.toFixed(1) || 0} miles</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">Total Driving:</span>
          <span className="font-medium">{tripData.total_driving_hours?.toFixed(1) || 0} hours</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">Total On-Duty:</span>
          <span className="font-medium">{tripData.total_on_duty_hours?.toFixed(1) || 0} hours</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">Trip Duration:</span>
          <span className="font-medium">{tripData.total_days || 0} days</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">Fuel Stops:</span>
          <span className="font-medium">{tripData.fuel_stops?.length || 0}</span>
        </div>
      </div>
    </div>
  );
}

export default TripSummary;
