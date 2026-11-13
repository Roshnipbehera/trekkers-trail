/**
 * ML INFERENCE SERVICE
 * Loads trained regression parameters and computes real-time atmospheric signal attenuation.
 */

const fs = require('fs');
const path = require('path');

let modelData = null;

try {
  const modelPath = path.join(__dirname, 'trained_model.json');
  if (fs.existsSync(modelPath)) {
    modelData = JSON.parse(fs.readFileSync(modelPath, 'utf8'));
  }
} catch (err) {
  console.warn("⚠️ Warning: Could not load trained_model.json, using fallback coefficients:", err.message);
}

// Fallback coefficients if JSON is absent
const defaultCoefficients = {
  elevation_angle_deg: -0.065,
  frequency_ghz: 0.162,
  rain_rate_mm_hr: 0.472,
  cloud_liquid_water_g_m3: 0.055,
  surface_temp_c: 0.004,
  relative_humidity_pct: 0.001
};
const defaultIntercept = 0.85;

/**
 * Predict signal attenuation (dB) from weather telemetry
 */
function predictAttenuation(features) {
  const coefs = modelData?.linear_coefficients || defaultCoefficients;
  const intercept = modelData?.linear_intercept ?? defaultIntercept;

  const elevation = Number(features.elevation_angle_deg ?? 45.0);
  const frequency = Number(features.frequency_ghz ?? 14.2);
  const rainRate = Number(features.rain_rate_mm_hr ?? 0.0);
  const cloudWater = Number(features.cloud_liquid_water_g_m3 ?? 0.2);
  const temp = Number(features.surface_temp_c ?? 22.0);
  const humidity = Number(features.relative_humidity_pct ?? 50.0);

  // Linear inference
  let attenuation = intercept +
    (coefs.elevation_angle_deg * elevation) +
    (coefs.frequency_ghz * frequency) +
    (coefs.rain_rate_mm_hr * rainRate) +
    (coefs.cloud_liquid_water_g_m3 * cloudWater) +
    (coefs.surface_temp_c * temp) +
    (coefs.relative_humidity_pct * humidity);

  // Attenuation cannot be negative
  attenuation = Math.max(0.1, Number(attenuation.toFixed(2)));

  // Categorize signal quality
  let quality = "OPTIMAL";
  let effectiveCapacityRatio = 1.0;

  if (attenuation > 6.0) {
    quality = "SEVERE_FADE";
    effectiveCapacityRatio = 0.55; // 45% bandwidth loss due to retransmissions
  } else if (attenuation > 2.5) {
    quality = "DEGRADED";
    effectiveCapacityRatio = 0.80; // 20% bandwidth degradation
  }

  return {
    attenuation_db: attenuation,
    quality_status: quality,
    effective_bandwidth_ratio: effectiveCapacityRatio,
    inputs: { elevation, frequency, rainRate, cloudWater, temp, humidity }
  };
}

function getModelMetadata() {
  return modelData || {
    model_name: "AtmosphericSignalLossPredictor",
    status: "active (fallback loaded)"
  };
}

module.exports = {
  predictAttenuation,
  getModelMetadata
};

