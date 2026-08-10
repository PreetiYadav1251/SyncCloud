import "dotenv/config";

import Fastify from "fastify";
import cors from "@fastify/cors";
import jwt from "@fastify/jwt";

import { authRoutes } from "./routes/auth.js";
import { prisma } from "./lib/prisma.js";

const app = Fastify({
  logger: true,
});

// --------------------------------------------------
// CORS
// --------------------------------------------------

await app.register(cors, {
  origin: true,
});

// --------------------------------------------------
// JWT
// --------------------------------------------------

const jwtSecret = process.env.JWT_SECRET;

if (!jwtSecret) {
  throw new Error("JWT_SECRET is not defined in .env");
}

await app.register(jwt, {
  secret: jwtSecret,
});

// --------------------------------------------------
// ROUTES
// --------------------------------------------------

app.get("/", async () => {
  return {
    message: "SyncCloud API is running 🚀",
  };
});

app.get("/api/health", async () => {
  return {
    status: "ok",
    service: "synccloud-api",
  };
});

// --------------------------------------------------
// DATABASE HEALTH
// --------------------------------------------------

app.get("/api/db-health", async (request, reply) => {
  try {
    await prisma.$queryRaw`SELECT 1`;

    return {
      status: "ok",
      database: "connected",
    };
  } catch (error) {
    request.log.error(error);

    return reply.status(500).send({
      status: "error",
      database: "disconnected",
    });
  }
});

// --------------------------------------------------
// AUTH ROUTES
// --------------------------------------------------

await app.register(authRoutes, {
  prefix: "/api/auth",
});

// --------------------------------------------------
// START SERVER
// --------------------------------------------------

const PORT = Number(process.env.PORT) || 4000;

try {
  await app.listen({
    port: PORT,
    host: "0.0.0.0",
  });

  console.log(`🚀 SyncCloud API running on http://localhost:${PORT}`);
} catch (error) {
  app.log.error(error);
  process.exit(1);
}