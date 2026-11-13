const express = require('express');
const router = express.Router();
const citizenController = require('../controllers/citizenController');
const { validate, CitizenRequestSchema } = require('../middleware/validator');

// GET /api/v1/citizen/requests - Retrieve all queued citizen requests
router.get('/requests', citizenController.getCitizenRequests);

// POST /api/v1/citizen/requests - Submit a new observation request (with Zod validation)
router.post('/requests', validate(CitizenRequestSchema), citizenController.createCitizenRequest);

module.exports = router;

