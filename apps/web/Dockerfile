# FROM node:22-alpine

# WORKDIR /app

# RUN corepack enable

# COPY . .

# RUN pnpm install --frozen-lockfile

# WORKDIR /app/apps/web

# EXPOSE 3000

# CMD ["pnpm", "dev", "--hostname", "0.0.0.0", "--port", "3000"]



FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]