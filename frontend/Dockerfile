# --- Etapa 1: build ---
FROM node:22-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# URL del backend-api en tiempo de BUILD (queda embebida en el JS estático).
# Pasar con --build-arg VITE_API_URL=https://tu-dominio/api
ARG VITE_API_URL=http://localhost:8005
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# --- Etapa 2: runtime ---
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
