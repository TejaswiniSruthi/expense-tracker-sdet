FROM node:22-alpine

WORKDIR /app

# install deps first — this layer caches unless package.json changes
COPY package*.json ./
RUN npm ci --omit=dev

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]