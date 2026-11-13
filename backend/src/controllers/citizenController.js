/**
 * CITIZEN CONTROLLER
 * Exposes endpoints for citizens to create and monitor Earth observation tasks.
 */

const citizenService = require('../services/citizenService');

function getCitizenRequests(req, res) {
  const requests = citizenService.getAllRequests();
  res.json({
    success: true,
    count: requests.length,
    data: requests
  });
}

function createCitizenRequest(req, res) {
  const newRequest = citizenService.addRequest(req.validatedBody);
  res.status(201).json({
    success: true,
    message: "Citizen observation request queued successfully",
    data: newRequest
  });
}

module.exports = {
  getCitizenRequests,
  createCitizenRequest
};

