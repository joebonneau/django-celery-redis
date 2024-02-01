FROM node:latest

WORKDIR /app/frontend

COPY . /app

RUN npm install

RUN chmod +x /app/deploy/docker/frontend/frontend-entrypoint-dev.sh
RUN chmod +x /app/deploy/docker/frontend/frontend-entrypoint-prod.sh

# Run start script when the container launches
# CMD ["npm", "run", "dev"]
