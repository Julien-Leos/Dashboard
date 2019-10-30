FROM node:lts-alpine
ADD . /app
WORKDIR /app/
RUN yarn install --force
EXPOSE 8080
CMD ["yarn", "serve"]