import React, { useState } from 'react';

function TripForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    current_location: 'Chicago, IL',
    pickup_location: 'Indianapolis, IN',
    dropoff_location: 'Atlanta, GA',
    cycle_used: 35
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'cycle_used' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-xl font-semibold text-[#1d1d1f]">Plan New Trip</h2>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">📍 Current Location</label>
        <input
          type="text"
          name="current_location"
          value={formData.current_location}
          onChange={handleChange}
          className="mac-input"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">📦 Pickup Location</label>
        <input
          type="text"
          name="pickup_location"
          value={formData.pickup_location}
          onChange={handleChange}
          className="mac-input"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">🏁 Dropoff Location</label>
        <input
          type="text"
          name="dropoff_location"
          value={formData.dropoff_location}
          onChange={handleChange}
          className="mac-input"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">⏱️ Current Cycle Used (hours)</label>
        <input
          type="number"
          name="cycle_used"
          value={formData.cycle_used}
          onChange={handleChange}
          min="0"
          max="70"
          step="0.5"
          className="mac-input"
        />
        <p className="text-xs text-gray-500 mt-1">Hours already worked in last 8 days (0-70)</p>
      </div>

      <button type="submit" disabled={loading} className="mac-button w-full">
        {loading ? 'Calculating...' : 'Plan Trip →'}
      </button>
    </form>
  );
}

export default TripForm;