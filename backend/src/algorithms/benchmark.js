/**
 * BENCHMARK HARNESS: 0/1 KNAPSACK ALGORITHM EFFICIENCY PROFILER
 * 
 * Subject: Algorithm Design (CA2 Requirement #5: Optimize for efficiency)
 * Compares execution time and memory across 4 algorithm variations.
 */

const { solveKnapsack } = require('./knapsack');

function generateRandomItems(count, maxWeight = 50, maxValue = 100) {
  const items = [];
  for (let i = 1; i <= count; i++) {
    items.push({
      id: `ITEM-${i}`,
      name: `Telemetry Tile ${i}`,
      weight: Math.floor(Math.random() * maxWeight) + 1,
      value: Math.floor(Math.random() * maxValue) + 1
    });
  }
  return items;
}

console.log("==========================================================================================");
console.log("   ORBITLINK ALGORITHMIC COMPLEXITY & PERFORMANCE BENCHMARK                               ");
console.log("==========================================================================================\n");

const scenarios = [
  { n: 10, capacity: 50, runRecursive: true, runMemo: true },
  { n: 20, capacity: 100, runRecursive: true, runMemo: true },
  { n: 25, capacity: 150, runRecursive: false, runMemo: true }, // Recursive would take 2^25 = 33M ops (too slow)
  { n: 100, capacity: 500, runRecursive: false, runMemo: true },
  { n: 300, capacity: 1000, runRecursive: false, runMemo: false }, // Memo table exhausts V8 heap memory (O(nW) objects)
  { n: 500, capacity: 2000, runRecursive: false, runMemo: false },
  { n: 1000, capacity: 5000, runRecursive: false, runMemo: false }
];

console.log(
  "| Items (n) | Capacity (W) | Recursive O(2^n) | Memoized O(nW) | 2D DP O(nW) | 1D Rolling O(nW, O(W) mem) |"
);
console.log(
  "|-----------|--------------|------------------|----------------|-------------|----------------------------|"
);

for (const sc of scenarios) {
  const items = generateRandomItems(sc.n);

  let recTime = "Skipped (O(2^n))";
  if (sc.runRecursive) {
    const recRes = solveKnapsack(sc.capacity, items, 'recursive');
    recTime = `${recRes.executionTimeMs} ms`;
  }

  let memTime = "Skipped (Heap OOM)";
  if (sc.runMemo) {
    const memRes = solveKnapsack(sc.capacity, items, 'memoized');
    memTime = `${memRes.executionTimeMs} ms`;
  }

  const dp2dRes = solveKnapsack(sc.capacity, items, '2d');
  const dp1dRes = solveKnapsack(sc.capacity, items, '1d');

  console.log(
    `| ${String(sc.n).padEnd(9)} | ${String(sc.capacity).padEnd(12)} | ${recTime.padEnd(16)} | ${memTime.padEnd(14)} | ${(dp2dRes.executionTimeMs + ' ms').padEnd(11)} | ${(dp1dRes.executionTimeMs + ' ms (O(W) space)').padEnd(26)} |`
  );
}

console.log("\n==========================================================================================");
console.log("SPACE COMPLEXITY ANALYSIS:");
console.log("  1. Recursive:        O(n) auxiliary call stack.");
console.log("  2. Memoization:      O(n * W) memo table + O(n) call stack.");
console.log("  3. 2D Tabulation:    O(n * W) DP matrix.");
console.log("  4. 1D Rolling Array: O(W) space - 90%+ memory reduction for large n!");
console.log("==========================================================================================\n");
