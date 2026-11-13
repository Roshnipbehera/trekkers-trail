/**
 * SATELLITE CONTROLLER
 * Exposes live constellation passes and ground station telemetry.
 */

const satelliteService = require('../services/satelliteService');

function getUpcomingPasses(req, res) {
  const passes = satelliteService.getUpcomingPasses();
  res.json({
    success: true,
    count: passes.length,
    data: passes
  });
}

function getFleetInfo(req, res) {
  res.json({
    success: true,
    satellites: satelliteService.getSatellites(),
    groundStations: satelliteService.getGroundStations()
  });
}

module.exports = {
  getUpcomingPasses,
  getFleetInfo
};

