import { useRef, useEffect } from 'react';
import { format } from 'date-fns';

function ELDLog({ dayNumber, date, drivingHours, onDutyHours, totalMiles, logEntries }) {
  const canvasRef = useRef(null);

  const formatDate = (dateStr) => {
    if (!dateStr) return '______';
    try {
      return format(new Date(dateStr), 'MM/dd/yyyy');
    } catch {
      return dateStr;
    }
  };

  // Status order for the grid rows
  const statusRows = ['off_duty', 'sleeper', 'driving', 'on_duty'];
  const statusLabels = {
    off_duty: 'OFF DUTY',
    sleeper: 'SLEEPER BERTH',
    driving: 'DRIVING',
    on_duty: 'ON DUTY (not driving)'
  };

  // Define drawLogGrid BEFORE using it in useEffect
  const drawLogGrid = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    console.log(`📊 Drawing ELD log for Day ${dayNumber}`, { logEntries });

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Grid dimensions
    const startX = 60;
    const startY = 40;
    const cellWidth = (width - startX - 40) / 24; // 24 hours
    const rowHeight = 35;
    
    // Draw background
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, width, height);
    
    // Draw hour labels (top row)
    ctx.fillStyle = '#333';
    ctx.font = '10px monospace';
    for (let hour = 0; hour <= 24; hour++) {
      const x = startX + (hour * cellWidth);
      ctx.fillText(hour.toString(), x - 4, startY - 5);
      
      // Draw vertical grid line
      ctx.beginPath();
      ctx.strokeStyle = '#ddd';
      ctx.lineWidth = 0.5;
      ctx.moveTo(x, startY);
      ctx.lineTo(x, startY + rowHeight * 4);
      ctx.stroke();
    }
    
    // Draw row labels and horizontal lines
    statusRows.forEach((status, idx) => {
      const y = startY + (idx * rowHeight);
      
      // Row label
      ctx.fillStyle = '#333';
      ctx.font = 'bold 10px monospace';
      ctx.fillText(statusLabels[status], 5, y + 15);
      
      // Horizontal grid line
      ctx.beginPath();
      ctx.strokeStyle = '#ddd';
      ctx.lineWidth = 0.5;
      ctx.moveTo(startX, y);
      ctx.lineTo(width - 20, y);
      ctx.stroke();
      
      // Draw the filled blocks for this row
      logEntries.forEach(entry => {
        if (entry.status === status) {
          const [startHour, startMin] = entry.start.split(':').map(Number);
          const [endHour, endMin] = entry.end.split(':').map(Number);
          
          const startDecimal = startHour + startMin / 60;
          let endDecimal = endHour + endMin / 60;
          if (endDecimal === 0) endDecimal = 24;
          
          const startXPos = startX + (startDecimal * cellWidth);
          const endXPos = startX + (endDecimal * cellWidth);
          const widthPos = endXPos - startXPos;
          
          // Choose color based on status
          let fillColor;
          switch(status) {
            case 'off_duty':
              fillColor = '#4ade80'; // Green
              break;
            case 'sleeper':
              fillColor = '#60a5fa'; // Blue
              break;
            case 'driving':
              fillColor = '#f87171'; // Red
              break;
            case 'on_duty':
              fillColor = '#fbbf24'; // Yellow
              break;
            default:
              fillColor = '#cbd5e1';
          }
          
          ctx.fillStyle = fillColor;
          ctx.fillRect(startXPos, y + 1, widthPos, rowHeight - 2);
        }
      });
    });
    
    // Draw bottom border
    ctx.beginPath();
    ctx.strokeStyle = '#999';
    ctx.lineWidth = 1;
    ctx.moveTo(startX, startY + rowHeight * 4);
    ctx.lineTo(width - 20, startY + rowHeight * 4);
    ctx.stroke();
  };

  // Now useEffect can safely call drawLogGrid
  useEffect(() => {
    if (logEntries && logEntries.length > 0) {
      console.log(`🎨 Day ${dayNumber}: Rendering ELD grid with ${logEntries.length} entries`);
      drawLogGrid();
    }
  }, [logEntries, dayNumber, drawLogGrid]);

  return (
    <div className="border border-gray-200 rounded-xl overflow-hidden bg-white">
      {/* Log Header */}
      <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
        <div className="flex justify-between items-center flex-wrap gap-2">
          <h3 className="font-semibold text-[#1d1d1f]">Day {dayNumber} Log</h3>
          <div className="text-sm text-gray-500 space-x-3">
            <span>📅 {formatDate(date)}</span>
            <span>📊 {totalMiles || 0} miles</span>
            <span>🚗 {drivingHours || 0}h driving</span>
            <span>💼 {onDutyHours || 0}h on-duty</span>
          </div>
        </div>
      </div>

      {/* Log Canvas Grid */}
      <div className="p-4">
        <canvas
          ref={canvasRef}
          width={900}
          height={200}
          className="w-full border border-gray-200 rounded-lg"
          style={{ backgroundColor: '#fff' }}
        />
        
        {/* Legend */}
        <div className="flex justify-center gap-6 mt-3 text-xs">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#4ade80' }}></div>
            <span>Off Duty</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#60a5fa' }}></div>
            <span>Sleeper Berth</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#f87171' }}></div>
            <span>Driving</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#fbbf24' }}></div>
            <span>On Duty (Not Driving)</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ELDLog;