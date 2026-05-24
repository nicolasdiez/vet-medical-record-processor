# src/frontend/Dockerfile

# ==========================================
# Stage 1: Build the React application
# ==========================================
FROM node:20-alpine AS build

# Set working directory inside the container
WORKDIR /app

# Copy package.json and install dependencies (leverage Docker cache)
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Vite project for production
RUN npm run build

# ==========================================
# Stage 2: Serve the application with Nginx
# ==========================================
FROM nginx:alpine

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the static build artifacts from the Stage 1 (build)
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]