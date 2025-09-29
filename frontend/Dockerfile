FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies first
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend
COPY . .

# Build the frontend
RUN npm run build

# Serve with nginx
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
