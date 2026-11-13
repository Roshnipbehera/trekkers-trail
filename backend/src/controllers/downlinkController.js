/**
 * DOWNLINK CONTROLLER
 * Bridges:
 *   1. Citizen Queued Orders
 *   2. ML Atmospheric Weather Attenuation
 *   3. 0/1 Knapsack Optimization Engine
 */

const citizenService = require('../services/citizenService');
const mlService = require('../services/mlService');
const { solveKnapsack } = require('../algorithms/knapsack');

function optimizeDownlink(req, res) {
  const { capacityMB, algorithmVariant = '1d', weatherTelemetry } = req.validatedBody;

  // STEP 1: Assess weather and predict rain-fade / atmospheric signal loss via ML
  let weatherAssessment = null;
  let effectiveCapacity = capacityMB;

  if (weatherTelemetry) {
    weatherAssessment = mlService.predictAttenuation(weatherTelemetry);
    effectiveCapacity = Math.floor(capacityMB * weatherAssessment.effective_bandwidth_ratio);
  }

  // STEP 2: Fetch pending citizen requests and format as knapsack items
  const allRequests = citizenService.getAllRequests();
  const items = allRequests.map(reqItem => ({
    id: reqItem.id,
    name: reqItem.title,
    weight: reqItem.weightMB,
    value: reqItem.priorityScore,
    category: reqItem.category,
    requestedBy: reqItem.requestedBy
  }));

  // STEP 3: Execute the 0/1 Knapsack Optimization Engine
  const optimizationResult = solveKnapsack(effectiveCapacity, items, algorithmVariant);

  // STEP 4: Calculate system performance KPIs
  const totalOfferedWeight = items.reduce((sum, it) => sum + it.weight, 0);
  const bandwidthUtilizationPct = Number(((optimizationResult.totalWeight / effectiveCapacity) * 100).toFixed(1));
  const emergencyRequestsIncluded = optimizationResult.selectedItems.filter(it => it.category === 'disaster').length;
  const totalEmergencyRequests = items.filter(it => it.category === 'disaster').length;

  res.json({
    success: true,
    data: {
      nominalCapacityMB: capacityMB,
      effectiveCapacityMB: effectiveCapacity,
      weatherImpact: weatherAssessment ? {
        predictedAttenuationDB: weatherAssessment.attenuation_db,
        signalQuality: weatherAssessment.quality_status,
        bandwidthRetainedRatio: weatherAssessment.effective_bandwidth_ratio
      } : "No weather telemetry provided (100% nominal capacity)",
      optimization: {
        algorithmUsed: optimizationResult.algorithm,
        spaceComplexity: optimizationResult.spaceComplexity || "O(nW)",
        executionTimeMs: optimizationResult.executionTimeMs,
        memoryDeltaBytes: optimizationResult.memoryDeltaBytes,
        totalItemsAvailable: items.length,
        itemsSelectedCount: optimizationResult.selectedItems.length,
        totalPayloadDownloadedMB: optimizationResult.totalWeight,
        totalPriorityValueEarned: optimizationResult.maxValue,
        bandwidthUtilizationPct: `${bandwidthUtilizationPct}%`,
        emergencyFulfillment: `${emergencyRequestsIncluded} / ${totalEmergencyRequests} Critical Requests Dispatched`,
        selectedOrders: optimizationResult.selectedItems
      }
    }
  });
}

module.exports = {
  optimizeDownlink
};

