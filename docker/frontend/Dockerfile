# ========= 1️⃣ Build Stage =========
FROM node:20-alpine AS builder

WORKDIR /app

# Copiamos primero los archivos de dependencias
COPY frontend/package.json frontend/yarn.lock ./

# Instalamos dependencias
RUN yarn install --frozen-lockfile --network-timeout 100000

# Copiamos el resto del proyecto
COPY frontend/ .

# Build en modo producción
RUN yarn build --configuration production

# ========= 2️⃣ Serve Stage =========
FROM nginx:alpine

# Limpiamos el contenido por defecto de nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiamos el build generado
COPY --from=builder /app/dist/frontend/browser /usr/share/nginx/html

# Copiamos la configuración personalizada de nginx
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf


EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
