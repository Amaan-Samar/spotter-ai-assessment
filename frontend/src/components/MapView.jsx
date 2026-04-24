import { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons in Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom icons for different locations
const pickupIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

const dropoffIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

const currentIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

const fuelIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

// Component to handle map zooming
function MapController({ center, zoom, onZoomToLocation }) {
  const map = useMap();
  
  useEffect(() => {
    if (center) {
      map.setView(center, zoom);
    }
  }, [center, zoom, map]);
  
  // Expose map instance to parent via ref
  useEffect(() => {
    if (onZoomToLocation) {
      onZoomToLocation(map);
    }
  }, [map, onZoomToLocation]);
  
  return null;
}

function MapView({ routeGeometry, pickup, dropoff, fuelStops = [] }) {
  const [mapInstance, setMapInstance] = useState(null);
  const [selectedLocation, setSelectedLocation] = useState(null);
  
  // Calculate center based on route geometry
  const defaultCenter = routeGeometry && routeGeometry.length > 0 
    ? [routeGeometry[0][0], routeGeometry[0][1]]
    : [39.8283, -98.5795];
  
  const [center] = useState(defaultCenter);
  const [zoom] = useState(6);

  // Log received data for debugging
  useEffect(() => {
    console.log('🗺️ MapView mounted with:', {
      routeGeometry,
      pickup,
      dropoff,
      fuelStops: fuelStops?.length || 0,
      hasGeometry: routeGeometry && routeGeometry.length > 0,
      geometryPoints: routeGeometry?.length
    });
  }, []);

  // Zoom to feature function
  const zoomToLocation = (coordinates, label) => {
    if (coordinates && mapInstance) {
      console.log(`🔍 Zooming to ${label}:`, coordinates);
      mapInstance.setView([coordinates[0], coordinates[1]], 10);
      setSelectedLocation(label);
      setTimeout(() => setSelectedLocation(null), 2000);
    }
  };

  return (
    <div className="relative rounded-xl overflow-hidden bg-gray-100" style={{ height: '450px', width: '100%' }}>
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
        zoomControl={true}
      >
        <MapController 
          center={center} 
          zoom={zoom} 
          onZoomToLocation={(map) => setMapInstance(map)}
        />
        
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Draw the route line if geometry exists */}
        {routeGeometry && routeGeometry.length > 0 && (
          <Polyline
            positions={routeGeometry}
            color="#007aff"
            weight={4}
            opacity={0.8}
          />
        )}
        
        {/* Add markers for each location */}
        {routeGeometry && routeGeometry.map((position, idx) => {
          let icon = currentIcon;
          let label = 'Current Location';
          
          if (idx === 0) {
            icon = currentIcon;
            label = '📍 Current Location';
          } else if (idx === 1) {
            icon = pickupIcon;
            label = '📦 Pickup Location';
          } else if (idx === routeGeometry.length - 1) {
            icon = dropoffIcon;
            label = '🏁 Dropoff Location';
          }
          
          return (
            <Marker key={idx} position={[position[0], position[1]]} icon={icon}>
              <Popup>
                <div className="text-sm">
                  <strong>{label}</strong><br />
                  Lat: {position[0].toFixed(4)}<br />
                  Lng: {position[1].toFixed(4)}
                </div>
              </Popup>
            </Marker>
          );
        })}
        
        {/* Add fuel stop markers */}
        {fuelStops && fuelStops.map((stop, idx) => (
          stop.latitude && stop.longitude ? (
            <Marker 
              key={`fuel-${idx}`} 
              position={[stop.latitude, stop.longitude]} 
              icon={fuelIcon}
            >
              <Popup>
                <div className="text-sm">
                  <strong>⛽ Fuel Stop</strong><br />
                  {stop.location || `Fuel stop at ${stop.miles} miles`}<br />
                  📍 {stop.miles} miles from start<br />
                  📅 Estimated: {stop.estimated_arrival || 'Day ' + (idx + 1)}
                </div>
              </Popup>
            </Marker>
          ) : null
        ))}
      </MapContainer>
      
      {/* Fixed Position Legend */}
      <div className="absolute bottom-3 right-3 bg-white/95 backdrop-blur-sm rounded-lg p-3 shadow-lg z-[1000] min-w-[180px] border border-gray-200">
        <div className="text-xs font-semibold text-gray-700 mb-2">Map Legend</div>
        <div className="space-y-1.5">
          <button 
            onClick={() => zoomToLocation(routeGeometry?.[0], 'Current')}
            className="flex items-center gap-2 text-xs hover:bg-gray-100 p-1.5 rounded w-full transition-colors"
          >
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span>Current Location</span>
          </button>
          <button 
            onClick={() => zoomToLocation(routeGeometry?.[1], 'Pickup')}
            className="flex items-center gap-2 text-xs hover:bg-gray-100 p-1.5 rounded w-full transition-colors"
          >
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span>Pickup Location</span>
          </button>
          <button 
            onClick={() => zoomToLocation(routeGeometry?.[routeGeometry?.length - 1], 'Dropoff')}
            className="flex items-center gap-2 text-xs hover:bg-gray-100 p-1.5 rounded w-full transition-colors"
          >
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span>Dropoff Location</span>
          </button>
          {fuelStops && fuelStops.length > 0 && (
            <div className="flex items-center gap-2 text-xs text-gray-600 pt-1 border-t border-gray-200 mt-1">
              <div className="w-3 h-3 rounded-full bg-orange-500"></div>
              <span>{fuelStops.length} Fuel Stop(s)</span>
            </div>
          )}
          <div className="flex items-center gap-2 text-xs text-gray-600">
            <div className="w-6 h-0.5 bg-blue-500"></div>
            <span>Route Path</span>
          </div>
        </div>
      </div>
      
      {/* Zoom feedback notification */}
      {selectedLocation && (
        <div className="absolute top-3 left-1/2 transform -translate-x-1/2 bg-black/75 text-white text-xs px-3 py-1.5 rounded-full z-[1000] animate-pulse">
          Zooming to {selectedLocation}...
        </div>
      )}
    </div>
  );
}

export default MapView;