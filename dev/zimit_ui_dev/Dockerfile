FROM node:14-alpine

RUN apk --no-cache add yarn
WORKDIR /app
COPY package.json yarn.lock /app/
RUN yarn install && yarn cache clean
COPY *.js /app/
COPY public /app/public
COPY src /app/src
CMD ["yarn", "serve", "--host", "0.0.0.0", "--port", "80"]