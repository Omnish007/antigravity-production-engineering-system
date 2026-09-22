---
name: Vercel
category: deployment
baselineVersion: Vercel CLI 38+
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: Vercel CLI 38+
supportedVersions:
- 38+
- 37+
legacyVersions:
- 36+
prohibitedVersions:
- < 36
sources:
- https://vercel.com/docs
- https://vercel.com/docs/cli
---
# Vercel Deployment Profile

## 1. Scope
Applies to frontend, Jamstack, and full-stack applications deployed to the Vercel platform (primarily Next.js, SvelteKit, Nuxt, and Remix).

## 2. Detection Signals
- Files: `vercel.json`, `.vercelignore`
- Frameworks: Next.js (`next.config.js`), SvelteKit (`svelte.config.js`), Nuxt (`nuxt.config.ts`)

## 3. Supported-Version Policy
- Target: Current Vercel Platform standards (Node.js 20+ runtime, Vercel CLI v34+).

## 4. Core Architectural Guidance
- **Edge vs. Serverless Functions**:
  - Default to Serverless (Node.js runtime) for full Node.js API support, native libraries, and reliable database connection pooling.
  - Use Edge Runtime only for lightweight, latency-critical middleware, geolocation routing, or fast redirects.
- **Connection Pooling**: When connecting serverless functions to relational databases or MongoDB, use connection pooling proxies (Prisma Accelerate, Neon serverless, Supabase pooler, MongoDB Atlas connection pooling) to avoid exhausting database connections.
- **Caching & ISR**: Use Incremental Static Regeneration (ISR) and `revalidateTag` / `revalidatePath` to balance speed and data freshness.

## 5. Security & Performance Guidance
- **Security Headers**: Configure HTTP security headers in `next.config.js` or `vercel.json` (HSTS, Content-Security-Policy, X-Frame-Options).
- **Environment Variables**: Configure sensitive secrets in Vercel Project Settings (encrypted); never commit `.env.production` to git.
- **Bundle Optimization**: Monitor deployment bundle size using Vercel Analytics and Speed Insights.

## 6. Testing Guidance
- Local Emulation: Test builds using `vercel build` or `vercel dev` locally to mirror cloud runtime behavior.
- Preview Deployments: Verify changes on Vercel preview environments before merging to production.

## 7. Common Anti-patterns
- Opening direct unpooled database connections from serverless functions, exhausting connection pools under traffic spikes.
- Using Edge Runtime for workloads that require Node.js native binaries or heavy cryptographic libraries.
- Relying on local in-memory state or filesystem storage across serverless function invocations.
- Storing environment secrets in repository files rather than Vercel environment variables.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://vercel.com/docs
- Vercel CLI Reference: https://vercel.com/docs/cli
- Local Inspection: Inspect `vercel.json` and project configuration files.
