# React UI Dockerfile
FROM hub.mirror.mojtabavi.dev/oven/bun:1-alpine

WORKDIR /app

# Copy package files
COPY package.json bun.lockb* ./

# Install dependencies
RUN bun install

# Copy application code
COPY . ./

# Expose Vite dev server port
EXPOSE 3000

# Environment variable for Vite
ENV HOST=0.0.0.0

# Start development server
CMD ["bun", "run", "dev", "--host", "0.0.0.0"]
