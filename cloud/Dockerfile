# ==============================================================================
# ORBITLINK - MULTI-STAGE PRODUCTION DOCKERFILE
# Subject: Cloud Computing (Virtualization & Containerization)
# ==============================================================================

# STAGE 1: Dependency & Build Stage
FROM node:20-alpine AS builder

WORKDIR /usr/src/app

# Install dependencies needed for node-gyp if any
RUN apk add --no-cache python3 make g++

# Copy package descriptors
COPY backend/package*.json ./

# Clean install production dependencies
RUN npm ci --only=production

# STAGE 2: Lightweight Production Runtime Image
FROM node:20-alpine AS runner

WORKDIR /usr/src/app

# Set Cloud-Native Environment Variables
ENV NODE_ENV=production
ENV PORT=5000

# Security Hardening: Run as non-root user (Principle of Least Privilege)
USER node

# Copy dependencies and application source from builder
COPY --chown=node:node --from=builder /usr/src/app/node_modules ./node_modules
COPY --chown=node:node backend/ ./

# Expose API Gateway Port
EXPOSE 5000

# Docker Healthcheck probe for Cloud Orchestrator (Kubernetes / AWS ECS)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:5000/api/health || exit 1

# Start OrbitLink Production Gateway
CMD ["node", "src/server.js"]

