const express = require('express');
const router = express.Router();
const satelliteController = require('../controllers/satelliteController');

// GET /api/v1/satellite/passes - Get live upcoming satellite passes
router.get('/passes', satelliteController.getUpcomingPasses);

// GET /api/v1/satellite/fleet - Get constellation and ground station fleet information
router.get('/fleet', satelliteController.getFleetInfo);

module.exports = router;

