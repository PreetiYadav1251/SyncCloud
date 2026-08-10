import { FastifyInstance } from "fastify";
import bcrypt from "bcryptjs";
import { prisma } from "../lib/prisma.js";

export async function authRoutes(app: FastifyInstance) {
  // REGISTER
  app.post("/register", async (request, reply) => {
    const body = request.body as {
      name?: string;
      email?: string;
      password?: string;
    };

    const name = body.name?.trim();
    const email = body.email?.trim().toLowerCase();
    const password = body.password;

    if (!name || !email || !password) {
      return reply.status(400).send({
        message: "Name, email and password are required",
      });
    }

    if (password.length < 8) {
      return reply.status(400).send({
        message: "Password must be at least 8 characters",
      });
    }

    const existingUser = await prisma.user.findUnique({
      where: {
        email,
      },
    });

    if (existingUser) {
      return reply.status(409).send({
        message: "Email is already registered",
      });
    }

    const passwordHash = await bcrypt.hash(password, 12);

    const user = await prisma.user.create({
      data: {
        name,
        email,
        passwordHash,
      },
      select: {
        id: true,
        name: true,
        email: true,
        createdAt: true,
      },
    });

    const token = app.jwt.sign({
      userId: user.id,
      email: user.email,
    });

    return reply.status(201).send({
      message: "Account created successfully",
      user,
      token,
    });
  });

  // LOGIN
  app.post("/login", async (request, reply) => {
    const body = request.body as {
      email?: string;
      password?: string;
    };

    const email = body.email?.trim().toLowerCase();
    const password = body.password;

    if (!email || !password) {
      return reply.status(400).send({
        message: "Email and password are required",
      });
    }

    const user = await prisma.user.findUnique({
      where: {
        email,
      },
    });

    if (!user) {
      return reply.status(401).send({
        message: "Invalid email or password",
      });
    }

    const passwordMatches = await bcrypt.compare(
      password,
      user.passwordHash
    );

    if (!passwordMatches) {
      return reply.status(401).send({
        message: "Invalid email or password",
      });
    }

    const token = app.jwt.sign({
      userId: user.id,
      email: user.email,
    });

    return reply.send({
      message: "Login successful",
      user: {
        id: user.id,
        name: user.name,
        email: user.email,
      },
      token,
    });
  });
}