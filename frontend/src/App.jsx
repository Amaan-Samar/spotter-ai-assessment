import React, { useState } from 'react';
import TripForm from './components/TripForm';
import MapView from './components/MapView';
import ELDLog from './components/ELDLog';
import TripSummary from './components/TripSummary';
import CycleTracker from './components/CycleTracker';
import { planTrip } from './services/api';
import 'leaflet/dist/leaflet.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [tripData, setTripData] = useState(null);
  const [error, setError] = useState(null);

  const handlePlanTrip = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await planTrip(formData);
      setTripData(result);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to plan trip');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#f5f5f7] to-[#e8e8ed]">
      {/* macOS Style Top Bar */}
      <div className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-[#ff5f57]"></div>
                <div className="w-3 h-3 rounded-full bg-[#febc2e]"></div>
                <div className="w-3 h-3 rounded-full bg-[#28c840]"></div>
              </div>
              <h1 className="text-xl font-semibold text-[#1d1d1f] ml-3">Spotter AI</h1>
            </div>
            <p className="text-sm text-gray-500">FMCSA HOS Compliant · 70hr/8day Rule</p>
          </div>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Input Section */}
        <div className="glass-card p-6 mb-6">
          <TripForm onSubmit={handlePlanTrip} loading={loading} />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
            <p className="text-red-600 text-sm">⚠️ {error}</p>
          </div>
        )}

        {tripData && (
          <>
            {/* Summary Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
              <div className="glass-card p-6">
                <TripSummary tripData={tripData} />
              </div>
              <div className="glass-card p-6 lg:col-span-2">
                <CycleTracker cycleData={tripData.cycle_tracking} />
              </div>
            </div>

            {/* Map Section */}
            <div className="glass-card p-6 mb-6">
              <h2 className="text-lg font-semibold mb-4 text-[#1d1d1f]">🗺️ Route Map</h2>
              <MapView 
                routeGeometry={tripData.route_geometry}
                pickup={tripData.days[0]?.start_location || 'Pickup'}
                dropoff={tripData.days[tripData.days.length - 1]?.end_location || 'Dropoff'}
                fuelStops={tripData.fuel_stops || []}
              />
            </div>

            {/* ELD Logs Section */}
            <div className="glass-card p-6">
              <h2 className="text-lg font-semibold mb-4 text-[#1d1d1f]">📋 ELD Daily Logs</h2>
              <div className="space-y-6">
                {tripData.days.map((day, index) => (
                  <ELDLog 
                    key={index}
                    dayNumber={day.day_number}
                    date={day.date}
                    drivingHours={day.driving_hours}
                    onDutyHours={day.on_duty_hours}
                    totalMiles={day.total_miles}
                    logEntries={day.log_entries}
                  />
                ))}
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;