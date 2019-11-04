FROM node:lts-alpine
WORKDIR /app
COPY . /app
RUN yarn install --force
EXPOSE 8080
CMD ["yarn", "serve"]