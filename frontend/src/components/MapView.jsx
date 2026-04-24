import React from 'react';

function MapView({ routeGeometry, pickup, dropoff }) {
  return (
    <div className="bg-gray-100 rounded-xl p-8 text-center">
      <div className="text-gray-500 mb-4">
        🗺️ Map View Coming Soon
      </div>
      <div className="text-sm text-gray-400">
        Route from {pickup} to {dropoff}
      </div>
      {routeGeometry && routeGeometry.length > 0 && (
        <div className="text-xs text-gray-400 mt-2">
          Route points: {routeGeometry.length} locations
        </div>
      )}
    </div>
  );
}

export default MapView;
