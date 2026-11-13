/**
 * ANALYTICS CONTROLLER
 * Exposes ML predictions and model benchmarking statistics.
 */

const mlService = require('../services/mlService');

function predictAtmosphericLoss(req, res) {
  const telemetry = req.validatedBody;
  const prediction = mlService.predictAttenuation(telemetry);

  res.json({
    success: true,
    data: prediction
  });
}

function getModelBenchmark(req, res) {
  const metadata = mlService.getModelMetadata();
  res.json({
    success: true,
    data: metadata
  });
}

module.exports = {
  predictAtmosphericLoss,
  getModelBenchmark
};

