const express = require('express');
const router = express.Router();
const analyticsController = require('../controllers/analyticsController');
const { validate, WeatherInferenceSchema } = require('../middleware/validator');

// POST /api/v1/analytics/predict-loss - Run ML inference on weather parameters
router.post('/predict-loss', validate(WeatherInferenceSchema), analyticsController.predictAtmosphericLoss);

// GET /api/v1/analytics/model-stats - Retrieve ML model metrics, evaluation, and feature importances
router.get('/model-stats', analyticsController.getModelBenchmark);

module.exports = router;

