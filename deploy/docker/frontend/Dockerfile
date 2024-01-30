FROM node:latest

WORKDIR /app/frontend

ADD ./frontend /app/frontend

RUN npm install
RUN npm run build

# Run start script when the container launches
ENTRYPOINT ["npm", "run", "start"]
# ENTRYPOINT ["npm", "run", "start", "-H", "0.0.0.0", "-p", "3000"]
