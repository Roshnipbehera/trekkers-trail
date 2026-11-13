/**
 * AUTOMATED TEST SUITE: 0/1 KNAPSACK ALGORITHM
 * 
 * Subject: Algorithm Design (CA2 Requirement #4: Test with multiple test cases)
 */

const {
  knapsackRecursive,
  knapsackMemoized,
  knapsack2D,
  knapsackOptimized1D,
  solveKnapsack
} = require('./knapsack');

let testsPassed = 0;
let testsFailed = 0;

function assertEqual(actual, expected, testName) {
  if (actual === expected) {
    console.log(`  ✅ PASS: ${testName} (Result = ${actual})`);
    testsPassed++;
  } else {
    console.error(`  ❌ FAIL: ${testName} (Expected: ${expected}, Got: ${actual})`);
    testsFailed++;
  }
}

console.log("============================================================");
console.log("   ORBITLINK 0/1 KNAPSACK ALGORITHM TEST HARNESS            ");
console.log("============================================================\n");

// TEST CASE 1: Standard Textbook Verification
console.log("Test Case 1: Classic Knapsack Verification");
const items1 = [
  { id: 'ORD-1', name: 'Flood Map Alpha', weight: 2, value: 3 },
  { id: 'ORD-2', name: 'Crop Survey Beta', weight: 3, value: 4 },
  { id: 'ORD-3', name: 'Wildfire Thermal Scan', weight: 4, value: 5 },
  { id: 'ORD-4', name: 'Urban Map Gamma', weight: 5, value: 6 }
];
const cap1 = 5; // Expected: item 1 (w=2,v=3) + item 2 (w=3,v=4) -> total weight 5, total value 7
assertEqual(knapsack2D(cap1, items1).maxValue, 7, "2D DP Max Value");
assertEqual(knapsackOptimized1D(cap1, items1).maxValue, 7, "1D Optimized DP Max Value");
assertEqual(knapsackMemoized(cap1, items1).maxValue, 7, "Memoized DP Max Value");
assertEqual(knapsackRecursive(cap1, items1, items1.length).maxValue, 7, "Recursive Brute Force Max Value");

// TEST CASE 2: Zero Capacity Edge Case
console.log("\nTest Case 2: Zero Capacity Edge Case (W = 0)");
assertEqual(knapsackOptimized1D(0, items1).maxValue, 0, "Zero capacity yields zero value");
assertEqual(knapsackOptimized1D(0, items1).selectedItems.length, 0, "Zero items selected when capacity is 0");

// TEST CASE 3: All Items Exceed Capacity
console.log("\nTest Case 3: All Items Exceed Capacity");
const heavyItems = [
  { id: 'HEAVY-1', name: 'Super-Res 8K Map', weight: 50, value: 100 },
  { id: 'HEAVY-2', name: 'SAR Radar Scan', weight: 80, value: 200 }
];
assertEqual(knapsackOptimized1D(20, heavyItems).maxValue, 0, "No items selected if all exceed capacity");

// TEST CASE 4: Capacity Fits All Items
console.log("\nTest Case 4: High Capacity Fits All Items");
const capAll = 100;
const totalVal = items1.reduce((sum, it) => sum + it.value, 0);
assertEqual(knapsackOptimized1D(capAll, items1).maxValue, totalVal, "Picks all items when capacity is abundant");

// TEST CASE 5: Realistic Satellite Ground-Pass Scenario
console.log("\nTest Case 5: Realistic LEO Satellite Downlink Pass (15 Citizen Requests)");
const satellitePassItems = [
  { id: 'CIT-01', name: 'Wildfire Perimeter (Triage Emergency)', weight: 450, value: 25, category: 'disaster' },
  { id: 'CIT-02', name: 'River Flood Basin Level (Triage Emergency)', weight: 400, value: 25, category: 'disaster' },
  { id: 'CIT-03', name: 'Drought Farm Moisture Index', weight: 250, value: 7, category: 'agriculture' },
  { id: 'CIT-04', name: 'Vineyard Disease Scan', weight: 220, value: 6, category: 'agriculture' },
  { id: 'CIT-05', name: 'Mountain Trail Avalanche Check', weight: 300, value: 5, category: 'trail' },
  { id: 'CIT-06', name: 'Coastal Erosion Observation', weight: 350, value: 4, category: 'environment' },
  { id: 'CIT-07', name: 'City Urban Growth Tile', weight: 500, value: 4, category: 'commercial' },
  { id: 'CIT-08', name: 'University Campus Aerial', weight: 180, value: 2, category: 'casual' },
  { id: 'CIT-09', name: 'Private Estate View', weight: 210, value: 2, category: 'casual' },
  { id: 'CIT-10', name: 'Stargazer Space Radar Snapshot', weight: 120, value: 1, category: 'casual' }
];
// Ground Station pass has 1000 MB (1 GB) capacity
const passCap = 1000;
const solverResult = solveKnapsack(passCap, satellitePassItems, '1d');

console.log(`  Optimization Result:`);
console.log(`    - Total Items Available: ${satellitePassItems.length}`);
console.log(`    - Items Selected: ${solverResult.selectedItems.length}`);
console.log(`    - Total Payload Weight: ${solverResult.totalWeight} MB / ${passCap} MB`);
console.log(`    - Total Priority Value Earned: ${solverResult.maxValue}`);
console.log(`    - Execution Time: ${solverResult.executionTimeMs} ms`);

// Assert total weight does not exceed capacity
if (solverResult.totalWeight <= passCap) {
  console.log(`  ✅ PASS: Weight constraint respected (${solverResult.totalWeight} <= ${passCap})`);
  testsPassed++;
} else {
  console.error(`  ❌ FAIL: Capacity exceeded!`);
  testsFailed++;
}

// Assert disaster triage items were selected (highest priority)
const hasDisaster1 = solverResult.selectedItems.some(i => i.id === 'CIT-01');
const hasDisaster2 = solverResult.selectedItems.some(i => i.id === 'CIT-02');
if (hasDisaster1 && hasDisaster2) {
  console.log(`  ✅ PASS: Life-safety emergency requests successfully prioritized`);
  testsPassed++;
} else {
  console.error(`  ❌ FAIL: Emergency items were not prioritized`);
  testsFailed++;
}

console.log("\n============================================================");
console.log(`SUMMARY: ${testsPassed} PASSED, ${testsFailed} FAILED`);
console.log("============================================================\n");

if (testsFailed > 0) {
  process.exit(1);
}
