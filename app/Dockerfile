FROM node:lts-alpine
ADD . /app
WORKDIR /app/
RUN yarn install --force
CMD ["yarn", "serve"]