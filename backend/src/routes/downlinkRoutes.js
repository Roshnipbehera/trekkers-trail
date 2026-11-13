const express = require('express');
const router = express.Router();
const downlinkController = require('../controllers/downlinkController');
const { validate, OptimizeDownlinkSchema } = require('../middleware/validator');

// POST /api/v1/downlink/optimize - Execute 0/1 Knapsack optimization on pass window
router.post('/optimize', validate(OptimizeDownlinkSchema), downlinkController.optimizeDownlink);

module.exports = router;

