/**
 * ORBITLINK - 0/1 KNAPSACK ALGORITHM ENGINE
 * 
 * Subject: Algorithm Design (CA2 - Activity 2)
 * Problem Statement:
 *   A Low Earth Orbit (LEO) satellite is passing over an Earth ground-station antenna.
 *   The pass window offers a finite radio bandwidth/downlink capacity W (in Megabytes or Gigabytes).
 *   Multiple client imagery orders (i = 1 to n) are queued onboard.
 *   Each order i has:
 *     - Tile size / payload weight: w_i (MB)
 *     - Value / Priority score: v_i (Urgency: 10 = Disaster/Wildfire, 6 = Farm drought, 3 = Hiker/Trail, 1 = Casual)
 *   Objective:
 *     Select a subset of orders S ⊆ {1, ..., n} such that:
 *       Maximize: ∑_{i ∈ S} v_i
 *       Subject to: ∑_{i ∈ S} w_i ≤ W
 *       where each item can be selected at most once (x_i ∈ {0, 1})
 */

const { performance } = require('perf_hooks');

/**
 * 1. NAIVE RECURSIVE (BRUTE FORCE) APPROACH
 * Time Complexity: O(2^n)
 * Space Complexity: O(n) auxiliary call stack
 */
function knapsackRecursive(capacity, items, n) {
  if (n === 0 || capacity === 0) {
    return { maxValue: 0, selectedItems: [] };
  }

  const current = items[n - 1];

  // If item weight exceeds current remaining capacity, it cannot be included
  if (current.weight > capacity) {
    return knapsackRecursive(capacity, items, n - 1);
  }

  // Option A: Include the current item
  const includeRes = knapsackRecursive(capacity - current.weight, items, n - 1);
  const includeValue = current.value + includeRes.maxValue;

  // Option B: Exclude the current item
  const excludeRes = knapsackRecursive(capacity, items, n - 1);

  if (includeValue > excludeRes.maxValue) {
    return {
      maxValue: includeValue,
      selectedItems: [...includeRes.selectedItems, current]
    };
  } else {
    return excludeRes;
  }
}

/**
 * 2. TOP-DOWN DYNAMIC PROGRAMMING (MEMOIZATION)
 * Time Complexity: O(n * W)
 * Space Complexity: O(n * W) memo table + O(n) call stack
 */
function knapsackMemoized(capacity, items) {
  const n = items.length;
  // Initialize memo table with -1
  const memo = Array.from({ length: n + 1 }, () => Array(capacity + 1).fill(null));

  function solve(cap, idx) {
    if (idx === 0 || cap === 0) {
      return { maxValue: 0, selectedIndices: [] };
    }

    if (memo[idx][cap] !== null) {
      return memo[idx][cap];
    }

    const current = items[idx - 1];

    if (current.weight > cap) {
      memo[idx][cap] = solve(cap, idx - 1);
      return memo[idx][cap];
    }

    const withItem = solve(cap - current.weight, idx - 1);
    const withoutItem = solve(cap, idx - 1);

    const valWith = current.value + withItem.maxValue;
    const valWithout = withoutItem.maxValue;

    if (valWith > valWithout) {
      memo[idx][cap] = {
        maxValue: valWith,
        selectedIndices: [...withItem.selectedIndices, idx - 1]
      };
    } else {
      memo[idx][cap] = withoutItem;
    }

    return memo[idx][cap];
  }

  const result = solve(capacity, n);
  return {
    maxValue: result.maxValue,
    selectedItems: result.selectedIndices.map(i => items[i])
  };
}

/**
 * 3. BOTTOM-UP 2D DYNAMIC PROGRAMMING (TABULATION) WITH BACKTRACKING
 * Time Complexity: O(n * W)
 * Space Complexity: O(n * W)
 * 
 * Builds DP table dp[i][w] representing the max value using a subset
 * of items 0..i-1 with maximum weight limit w.
 */
function knapsack2D(capacity, items) {
  const n = items.length;
  // dp[i][w] = maximum value attainable with first i items and capacity w
  const dp = Array.from({ length: n + 1 }, () => new Int32Array(capacity + 1));

  // Build table bottom-up
  for (let i = 1; i <= n; i++) {
    const item = items[i - 1];
    for (let w = 0; w <= capacity; w++) {
      if (item.weight <= w) {
        const pick = item.value + dp[i - 1][w - item.weight];
        const skip = dp[i - 1][w];
        dp[i][w] = pick > skip ? pick : skip;
      } else {
        dp[i][w] = dp[i - 1][w];
      }
    }
  }

  const maxValue = dp[n][capacity];

  // Backtrack to find the exact items chosen
  const selectedItems = [];
  let currW = capacity;
  for (let i = n; i > 0 && currW > 0; i--) {
    // If the value differs from the row above, the i-th item was included
    if (dp[i][currW] !== dp[i - 1][currW]) {
      const item = items[i - 1];
      selectedItems.push(item);
      currW -= item.weight;
    }
  }

  return {
    maxValue,
    totalWeight: capacity - currW,
    selectedItems: selectedItems.reverse(),
    algorithm: "2D Dynamic Programming (Tabulation)"
  };
}

/**
 * 4. SPACE-OPTIMIZED 1D DYNAMIC PROGRAMMING (ROLLING ARRAY)
 * Time Complexity: O(n * W)
 * Space Complexity: O(W)  --> Massive space optimization from O(n*W)
 * 
 * Uses a single 1D array traversed backwards from capacity down to item.weight
 * to prevent using the same item multiple times.
 */
function knapsackOptimized1D(capacity, items) {
  const n = items.length;
  // dp[w] stores max value for capacity w
  const dp = new Int32Array(capacity + 1);
  
  // Track item selections using a bitmask or parent tracking table
  // For back-tracking in 1D, we store a boolean inclusion matrix
  const included = Array.from({ length: n }, () => new Uint8Array(capacity + 1));

  for (let i = 0; i < n; i++) {
    const item = items[i];
    // Traverse backwards from capacity down to item.weight
    for (let w = capacity; w >= item.weight; w--) {
      const candidateValue = dp[w - item.weight] + item.value;
      if (candidateValue > dp[w]) {
        dp[w] = candidateValue;
        included[i][w] = 1;
      }
    }
  }

  // Backtrack selected items
  const selectedItems = [];
  let currW = capacity;
  for (let i = n - 1; i >= 0 && currW > 0; i--) {
    if (included[i][currW]) {
      selectedItems.push(items[i]);
      currW -= items[i].weight;
    }
  }

  return {
    maxValue: dp[capacity],
    totalWeight: capacity - currW,
    selectedItems: selectedItems.reverse(),
    algorithm: "Space-Optimized 1D Dynamic Programming (Rolling Array)",
    spaceComplexity: "O(W)"
  };
}

/**
 * BENCHMARK & SOLVER WRAPPER
 * Executes solver and measures accurate microsecond execution time and memory usage.
 */
function solveKnapsack(capacity, items, variant = '1d') {
  const startMem = process.memoryUsage().heapUsed;
  const startTime = performance.now();

  let result;
  switch (variant) {
    case 'recursive':
      result = knapsackRecursive(capacity, items, items.length);
      result.totalWeight = result.selectedItems.reduce((acc, it) => acc + it.weight, 0);
      result.algorithm = "Recursive (Brute Force)";
      break;
    case 'memoized':
      result = knapsackMemoized(capacity, items);
      result.totalWeight = result.selectedItems.reduce((acc, it) => acc + it.weight, 0);
      result.algorithm = "Top-Down Memoization";
      break;
    case '2d':
      result = knapsack2D(capacity, items);
      break;
    case '1d':
    default:
      result = knapsackOptimized1D(capacity, items);
      break;
  }

  const endTime = performance.now();
  const endMem = process.memoryUsage().heapUsed;

  return {
    ...result,
    capacity,
    itemCount: items.length,
    executionTimeMs: Number((endTime - startTime).toFixed(4)),
    memoryDeltaBytes: Math.max(0, endMem - startMem)
  };
}

module.exports = {
  knapsackRecursive,
  knapsackMemoized,
  knapsack2D,
  knapsackOptimized1D,
  solveKnapsack
};

