/**
 * SATELLITE & GROUND STATION SERVICE
 * Models LEO satellites, ground-station antennas, and upcoming pass windows.
 */

const SATELLITES = [
  { id: 'SAT-S2A', name: 'Sentinel-2A', type: 'Multispectral Optical', altitude_km: 786, band: 'Ka-band (26.5 GHz)' },
  { id: 'SAT-L9', name: 'Landsat-9', type: 'Thermal & Multispectral', altitude_km: 705, band: 'X-band (8.4 GHz)' },
  { id: 'SAT-TERRA', name: 'Terra-1 (EOS AM-1)', type: 'MODIS Climate & Wildfire', altitude_km: 705, band: 'X-band (8.4 GHz)' },
  { id: 'SAT-WV3', name: 'WorldView-3 (Commercial High-Res)', type: '30cm Optical', altitude_km: 617, band: 'Ka-band (26.5 GHz)' }
];

const GROUND_STATIONS = [
  { id: 'GS-BLR', name: 'Bangalore Deep Space Network', lat: 12.9716, lng: 77.5946, defaultCapacityMB: 1500 },
  { id: 'GS-SVA', name: 'Svalbard Arctic Ground Station', lat: 78.2297, lng: 15.4077, defaultCapacityMB: 3000 },
  { id: 'GS-FBK', name: 'Fairbanks Alaska Telemetry Station', lat: 64.8378, lng: -147.7164, defaultCapacityMB: 2000 }
];

function getUpcomingPasses() {
  const now = new Date();
  return SATELLITES.map((sat, idx) => {
    const station = GROUND_STATIONS[idx % GROUND_STATIONS.length];
    const minutesToPass = (idx + 1) * 18 + Math.floor(Math.random() * 10);
    const durationMinutes = 8 + (idx % 4);
    const passStartTime = new Date(now.getTime() + minutesToPass * 60000);
    const passEndTime = new Date(passStartTime.getTime() + durationMinutes * 60000);

    return {
      passId: `PASS-${sat.id}-${Date.now().toString().slice(-4)}`,
      satellite: sat,
      groundStation: station,
      minutesUntilPass: minutesToPass,
      durationMinutes,
      maxElevationAngleDeg: 45 + (idx * 12),
      nominalCapacityMB: station.defaultCapacityMB,
      startTime: passStartTime.toISOString(),
      endTime: passEndTime.toISOString()
    };
  });
}

function getSatellites() {
  return SATELLITES;
}

function getGroundStations() {
  return GROUND_STATIONS;
}

module.exports = {
  SATELLITES,
  GROUND_STATIONS,
  getUpcomingPasses,
  getSatellites,
  getGroundStations
};

