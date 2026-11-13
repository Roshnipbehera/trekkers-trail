/**
 * REQUEST VALIDATION MIDDLEWARE (ZOD)
 * Enforces strict typing and contract validation on incoming request bodies.
 */

const { z } = require('zod');

// Schema for Citizen Observation Request
const CitizenRequestSchema = z.object({
  title: z.string().min(3, "Title must be at least 3 characters").max(100),
  category: z.enum(['disaster', 'agriculture', 'trail', 'casual'], {
    errorMap: () => ({ message: "Category must be one of: disaster, agriculture, trail, casual" })
  }),
  lat: z.number().min(-90).max(90),
  lng: z.number().min(-180).max(180),
  requestedBy: z.string().optional(),
  weightMB: z.number().positive().max(2000).optional()
});

// Schema for Downlink Optimization Request
const OptimizeDownlinkSchema = z.object({
  capacityMB: z.number().positive("Capacity must be greater than 0").max(10000),
  algorithmVariant: z.enum(['1d', '2d', 'memoized', 'recursive']).optional(),
  weatherTelemetry: z.object({
    rain_rate_mm_hr: z.number().min(0).max(100).optional(),
    elevation_angle_deg: z.number().min(5).max(90).optional(),
    frequency_ghz: z.number().positive().optional(),
    cloud_liquid_water_g_m3: z.number().min(0).optional(),
    surface_temp_c: z.number().optional(),
    relative_humidity_pct: z.number().min(0).max(100).optional()
  }).optional()
});

// Schema for Atmospheric ML Inference
const WeatherInferenceSchema = z.object({
  elevation_angle_deg: z.number().min(5).max(90).optional(),
  frequency_ghz: z.number().positive().optional(),
  rain_rate_mm_hr: z.number().min(0).max(100).optional(),
  cloud_liquid_water_g_m3: z.number().min(0).optional(),
  surface_temp_c: z.number().optional(),
  relative_humidity_pct: z.number().min(0).max(100).optional()
});

function validate(schema) {
  return (req, res, next) => {
    try {
      req.validatedBody = schema.parse(req.body);
      next();
    } catch (err) {
      if (err instanceof z.ZodError) {
        return res.status(400).json({
          success: false,
          error: {
            code: "VALIDATION_ERROR",
            message: "Invalid request payload",
            details: err.errors.map(e => ({ field: e.path.join('.'), issue: e.message }))
          }
        });
      }
      next(err);
    }
  };
}

module.exports = {
  validate,
  CitizenRequestSchema,
  OptimizeDownlinkSchema,
  WeatherInferenceSchema
};

