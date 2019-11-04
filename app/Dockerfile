FROM node:lts-alpine
WORKDIR /app/
COPY ./package.json .
RUN yarn install
CMD ["yarn", "serve"]