FROM node:latest

WORKDIR /app/frontend

COPY . /app

RUN npm install
# RUN npm run build

# Run start script when the container launches
CMD ["npm", "run", "dev"]
