FROM node:20-alpine

RUN apk --no-cache add yarn
WORKDIR /app
COPY ui/package.json ui/yarn.lock /app/
RUN yarn install
COPY ui/index.html /app/
COPY ui/*.json /app/
COPY ui/*.ts /app/
COPY ui/*.js /app/
COPY ui/public /app/public
COPY ui/src /app/src
COPY locales /locales
CMD ["yarn", "dev", "--host", "0.0.0.0", "--port", "80"]
