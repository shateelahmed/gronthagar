FROM node:21-alpine AS base

WORKDIR /src/frontend

COPY ./src/frontend/package*.json /

FROM base AS production
ENV NODE_ENV=production
RUN npm ci
COPY . /
CMD ["npm", "start"]

FROM base AS dev
ENV NODE_ENV=dev
RUN npm install
COPY . /
CMD ["npm", "start"]
