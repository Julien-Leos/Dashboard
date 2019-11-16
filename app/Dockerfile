FROM node:lts-alpine
WORKDIR /app
COPY . /app
RUN yarn cache clean
RUN yarn install --force
EXPOSE 3000
ENV HOST 0.0.0.0
CMD ["yarn", "dev"]