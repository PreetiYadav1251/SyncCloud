# FROM node:22-alpine

# WORKDIR /app

# RUN corepack enable

# COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
# COPY apps/web/package.json ./apps/web/package.json
# COPY packages ./packages

# RUN pnpm install --frozen-lockfile

# COPY apps/web ./apps/web

# WORKDIR /app/apps/web

# EXPOSE 3000

# CMD ["pnpm", "dev", "--hostname", "0.0.0.0"]


FROM node:22-alpine

WORKDIR /app

RUN corepack enable

COPY . .

RUN pnpm install --frozen-lockfile

WORKDIR /app/apps/web

EXPOSE 3000

CMD ["pnpm", "dev", "--hostname", "0.0.0.0", "--port", "3000"]