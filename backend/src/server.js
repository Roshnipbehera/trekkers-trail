/**
 * ORBITLINK - ENTERPRISE EXPRESS.JS API GATEWAY
 * 
 * Subject: Server Side Scripting (CA2 - Activity 2: Express.js Routing Application)
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const path = require('path');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
require('dotenv').config();

const { errorHandler } = require('./middleware/errorHandler');

// Route Imports
const citizenRoutes = require('./routes/citizenRoutes');
const downlinkRoutes = require('./routes/downlinkRoutes');
const analyticsRoutes = require('./routes/analyticsRoutes');
const satelliteRoutes = require('./routes/satelliteRoutes');

const app = express();
const PORT = process.env.PORT || 5000;

// 1. SECURITY & LOGGING MIDDLEWARE
app.use(helmet({
  contentSecurityPolicy: false // Allows loading Leaflet maps and CDNs in frontend
}));
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Rate limiting: 300 requests per 15 minutes
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 300,
  message: {
    success: false,
    error: {
      code: "RATE_LIMIT_EXCEEDED",
      message: "Too many requests from this IP, please try again after 15 minutes."
    }
  }
});
app.use('/api/', limiter);

// 2. STATIC ASSETS (CITIZEN WEB DASHBOARD)
app.use(express.static(path.join(__dirname, 'public')));

// 3. SWAGGER / OPENAPI DOCUMENTATION
try {
  const swaggerDocument = YAML.load(path.join(__dirname, 'swagger.yaml'));
  app.use('/api/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
  console.log("📖 Swagger UI documentation available at /api/docs");
} catch (err) {
  console.warn("⚠️ Could not load swagger.yaml:", err.message);
}

// 4. HEALTH CHECK ENDPOINT
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'OrbitLink API Gateway',
    timestamp: new Date().toISOString(),
    uptimeSeconds: Math.floor(process.uptime()),
    memoryUsageMB: Math.round(process.memoryUsage().heapUsed / 1024 / 1024)
  });
});

// 5. VERSIONED API ROUTES
app.use('/api/v1/citizen', citizenRoutes);
app.use('/api/v1/downlink', downlinkRoutes);
app.use('/api/v1/analytics', analyticsRoutes);
app.use('/api/v1/satellite', satelliteRoutes);

// Root fallback to serve dashboard
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 6. 404 CATCH-ALL ROUTE
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    error: {
      code: "NOT_FOUND",
      message: `The requested endpoint ${req.method} ${req.originalUrl} does not exist.`
    }
  });
});

// 7. CENTRALIZED ERROR HANDLING MIDDLEWARE
app.use(errorHandler);

// START SERVER
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log("============================================================");
    console.log(`🚀 OrbitLink Server running on http://localhost:${PORT}`);
    console.log(`🌐 Citizen Web Dashboard: http://localhost:${PORT}`);
    console.log(`📚 OpenAPI / Swagger Docs: http://localhost:${PORT}/api/docs`);
    console.log(`❤️ Healthcheck Endpoint:   http://localhost:${PORT}/api/health`);
    console.log("============================================================");
  });
}

module.exports = app;

