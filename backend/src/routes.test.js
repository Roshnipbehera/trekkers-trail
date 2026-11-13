/**
 * AUTOMATED INTEGRATION TESTS: EXPRESS.JS ROUTING APPLICATION
 * 
 * Subject: Server Side Scripting (CA2 - Express.js Routing Application)
 */

process.env.NODE_ENV = 'test';
const http = require('http');
const app = require('./server');

const server = app.listen(0, '127.0.0.1', async () => {
  const port = server.address().port;
  console.log(`Test server running on http://127.0.0.1:${port}`);

  let passed = 0;
  let failed = 0;

  async function testEndpoint(name, path, method = 'GET', body = null) {
    return new Promise((resolve) => {
      const options = {
        hostname: '127.0.0.1',
        port,
        path,
        method,
        headers: body ? { 'Content-Type': 'application/json' } : {}
      };

      const req = http.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            if (res.statusCode >= 200 && res.statusCode < 300 && (json.success !== false || json.status === 'healthy')) {
              console.log(`  ✅ PASS: ${method} ${path} (${res.statusCode}) - ${name}`);
              passed++;
            } else {
              console.error(`  ❌ FAIL: ${method} ${path} (${res.statusCode}) - Got: ${data}`);
              failed++;
            }
          } catch (e) {
            console.error(`  ❌ FAIL: ${method} ${path} (${res.statusCode}) - Invalid JSON: ${data}`);
            failed++;
          }
          resolve();
        });
      });

      req.on('error', (err) => {
        console.error(`  ❌ ERROR: ${method} ${path} - ${err.message}`);
        failed++;
        resolve();
      });

      if (body) req.write(JSON.stringify(body));
      req.end();
    });
  }

  console.log("============================================================");
  console.log("   ORBITLINK EXPRESS.JS INTEGRATION TEST HARNESS            ");
  console.log("============================================================\n");

  await testEndpoint("Healthcheck", "/api/health", "GET");
  await testEndpoint("List Citizen Requests", "/api/v1/citizen/requests", "GET");
  await testEndpoint("Create Citizen Request", "/api/v1/citizen/requests", "POST", {
    title: "Test Emergency Wildfire Scan",
    category: "disaster",
    lat: 13.0827,
    lng: 80.2707,
    requestedBy: "Automated Integration Tester"
  });
  await testEndpoint("Predict Atmospheric Loss", "/api/v1/analytics/predict-loss", "POST", {
    rain_rate_mm_hr: 20.0,
    elevation_angle_deg: 35.0,
    frequency_ghz: 26.5
  });
  await testEndpoint("Model Statistics", "/api/v1/analytics/model-stats", "GET");
  await testEndpoint("Upcoming Passes", "/api/v1/satellite/passes", "GET");
  await testEndpoint("Optimize Downlink (Knapsack)", "/api/v1/downlink/optimize", "POST", {
    capacityMB: 1200,
    algorithmVariant: "1d",
    weatherTelemetry: {
      rain_rate_mm_hr: 15.0,
      elevation_angle_deg: 40.0,
      frequency_ghz: 26.5
    }
  });

  console.log("\n============================================================");
  console.log(`INTEGRATION RESULTS: ${passed} PASSED, ${failed} FAILED`);
  console.log("============================================================\n");

  server.close(() => {
    process.exit(failed > 0 ? 1 : 0);
  });
});
