# FROM python:3.7-alpine
# WORKDIR /Back
# ENV FLASK_APP Back/app.py
# ENV FLASK_RUN_HOST 0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
# COPY Back/requirements.txt Back/requirements.txt
# RUN pip install -r Back/requirements.txt
# COPY . .
# CMD ["flask", "run"]

FROM node:lts-alpine
WORKDIR /front
COPY front/package.json ./package.json
COPY front/yarn.lock ./yarn.lock
RUN yarn install
COPY . .
EXPOSE 8080
CMD ["yarn", "serve"]