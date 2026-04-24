import React, { useState, useEffect } from 'react';
import { getTrips } from '../services/api';

function TripHistory({ onSelectTrip }) {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrips();
  }, []);

  const fetchTrips = async () => {
    try {
      const response = await getTrips();
      setTrips(response.trips || []);
    } catch (error) {
      console.error('Failed to fetch trips:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading history...</div>;

  return (
    <div className="glass-card p-6">
      <h2 className="text-lg font-semibold mb-4">📜 Trip History</h2>
      
      {trips.length === 0 ? (
        <p className="text-gray-500 text-center py-4">No trips planned yet</p>
      ) : (
        <div className="space-y-2">
          {trips.map((trip) => (
            <button
              key={trip.id}
              onClick={() => onSelectTrip(trip.id)}
              className="w-full text-left p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
            >
              <div className="flex justify-between items-center">
                <div>
                  <span className="font-medium">{trip.from}</span>
                  <span className="text-gray-400 mx-2">→</span>
                  <span className="font-medium">{trip.to}</span>
                </div>
                <div className="text-sm text-gray-500">
                  {trip.date} | {trip.miles} mi | {trip.days} days
                </div>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default TripHistory;