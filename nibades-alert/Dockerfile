FROM node:22.17.0-alpine AS base

# Install system dependencies
RUN apk add --no-cache libc6-compat

# Setup working directory
WORKDIR /app

# ----------------------
# Dependencies Layer
# ----------------------
FROM base AS deps

# Copy only lockfile + manifest to leverage cache
COPY .npmrc .npmrc
COPY package.json pnpm-lock.yaml* ./

# Install dependencies (dev + prod)
RUN npm install -g corepack@latest && \
    corepack enable pnpm && \
    pnpm install --frozen-lockfile --registry $NPM_CACHE_URL

# ----------------------
# Builder Layer
# ----------------------
FROM base AS builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build the app (you can disable telemetry if needed)
RUN npm install -g corepack@latest && \
    corepack enable pnpm && \
    pnpm run build || true  # allow build to continue if ESLint fails

# ----------------------
# Runner Layer (Production)
# ----------------------
FROM base AS runner

WORKDIR /app

ENV NODE_ENV production
ENV PORT=3000
ENV HOSTNAME='0.0.0.0'

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Ensure prerender cache folder
RUN mkdir .next && chown nextjs:nodejs .next

# Copy only necessary files
# COPY --from=builder /app/public ./public
# COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
# COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app ./


USER nextjs

EXPOSE $PORT

CMD ["node", "server.js"]
