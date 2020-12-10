FROM node:14-alpine as builder

RUN apk --no-cache add yarn
WORKDIR /src/ui
COPY ui/package.json ui/yarn.lock /src/ui/
RUN yarn install
COPY ui/*.js /src/ui/
COPY ui/public /src/ui/public
COPY ui/src /src/ui/src
RUN NODE_ENV=production yarn build

FROM tiangolo/uwsgi-nginx:python3.8

COPY --from=builder /src/ui/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN pip install -U pip
RUN pip install uwsgi==2.0.18

COPY api/requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY api/src /app/
WORKDIR /app/

ENV MONGODB_URI mongodb://localhost
ENV MAIN_PREFIX /api
ENV ZIMIT_API_URL /api/v1
ENV ZIMFARM_WEBAPI https://api.farm.youzim.it/v1
ENV INTERNAL_ZIMFARM_WEBAPI http://dispatcher.backend.zimit.kiwixoffline.node.intern/v1
ENV _ZIMFARM_USERNAME -
ENV _ZIMFARM_PASSWORD -

# max --limit for recipes
# ENV ZIMIT_LIMIT 100

# notifications
ENV MAILGUN_API_URL https://api.mailgun.net/v3/mg.youzim.it
ENV MAILGUN_FROM Youzim.it <info@youzim.it>
# ENV MAILGUN_API_KEY -
ENV PUBLIC_URL https://youzim.it
ENV PUBLIC_API_URL https://youzim.it/api/v1
# ENV HOOK_TOKEN somestring

# prestart script (former entrypoint - database init)
COPY api/prestart.sh /app/prestart.sh
RUN chmod +x /app/prestart.sh

# own entrypoint to dump vars into JS and prevent tiangolo's
ENTRYPOINT ["entrypoint.sh"]
CMD ["/start.sh"]
