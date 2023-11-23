This is a docker-compose configuration to be used **only** for development purpose. There is
almost zero security in the stack configuration.

It is composed of the Zimit frontend and API (of course), but also a local Zimfarm DB,
API and UI, so that you can test the whole integration locally.

Zimit UI and API are not deployed as they would be in production to allow hot reload of
most modifications done to the source code.

Zimfarm UI, API and DB are deployed with official production Docker images.

## List of containers

### zimit_ui

This container is Zimit frontend web server (UI only)

### zimit_api

This container is Zimit API server (API only)

## zimfarm_db

This container is a local Zimfarm database

## zimfarm_api

This container is a local Zimfarm API

## zimfarm_ui

This container is a local Zimfarm UI

## Instructions

First start the Docker-Compose stack:

```sh
cd dev
docker compose -p zimit up -d
```

If it is your first execution of the dev stack, you need to create a "virtual" worker in Zimfarm DB:

```sh
dev/create_worker.sh
```

If you have requested a task via Zimit UI and want to simulate a worker starting this task to observe the consequence in Zimit UI, you might use the `dev/start_first_req_task.sh`.

## Restart the backend

Should the API process fail, you might restart it with:
```sh
docker restart zimit-zimit_ui-1
```

## Browse the web UIs

You might open following URLs in your favorite browser:

- [Zimit UI](http://localhost:8001)
- [Zimfarm API](http://localhost:8002)
- [Zimfarm UI](http://localhost:8003)

You can login into Zimfarm UI with username `admin` and password `admin`.