# ========= 1️⃣ Build Stage =========
FROM node:20-alpine AS builder

WORKDIR /app

# Copiamos primero los archivos de dependencias
COPY package.json yarn.lock ./

# Instalamos dependencias
RUN yarn install --frozen-lockfile

# Copiamos el resto del proyecto
COPY . .

# Build en modo producción
RUN yarn build --configuration production

# ========= 2️⃣ Serve Stage =========
FROM nginx:alpine

# Limpiamos el contenido por defecto de nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiamos el build generado
COPY --from=builder /app/dist/frontend/browser /usr/share/nginx/html

# Copiamos la configuración personalizada de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf


EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
