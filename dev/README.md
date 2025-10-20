This is a docker-compose configuration to be used **only** for development purpose. There is
almost zero security in the stack configuration.

It is composed of the Zimit frontend UI and API (of course), but also a local Zimfarm DB,
API, worker and UI, so that you can test the whole integration locally.

Zimit frontend UI has two containers, one identical to production and one allowing hot reload
of local developments.

Zimit frontend API has one container, slightly modified to allow hot reload of
most modifications done to the source code.

Zimfarm UI, API worker, and DB are deployed with official production Docker images.

## List of containers

### zimit-ui-prod

This container is Zimit frontend UI as served in production (already compiled as a static website, so not possible to live-edit)

### zimit-ui-dev

This container is Zimit frontend UI served in development mode (possible to live-edit)

### zimit-api

This container is Zimit frontend API server (only slightly modified to enable live reload of edits)

## zimfarm-db

This container is a local Zimfarm database

## zimfarm-api

This container is a local Zimfarm API

## zimfarm-ui

This container is a local Zimfarm UI

## zimfarm-worker-manager

This container is a local Zimfarm worker manager. It pulls the Zimfarm task worker image to
execute tasks

## zimfarm-receiver

This container stores the uploaded files/logs for each task.

## Instructions

### Starting the Compose Stack

- To start the compose services (without the worker):

  ```sh
  cd dev
  docker compose up --build
  ```

- To start the compose services (with a registered worker):

  ```sh
  cd dev
  docker compose --profile worker up --build
  ```

- If you are running with worker profile, you will need to create warehouse paths to upload the logs and files for each task.
  ```sh
  docker exec -it zimfarm-receiver bash
  /contrib/create-warehouse-paths.sh
  ```

If it is your first execution of the dev stack, you need to create offliners and a "virtual" worker in Zimfarm DB. Thus, you need to start the services without the worker
profile till you register a worker.

- To create offliners:

  ```sh
  dev/create_offliners.sh
  ```

  This pulls the latest offliner definitions from the respective offliner repositories
  and registers them with the Zimfarm API. The versions of the offliner definitions
  are hardcoded to "dev". This is the same as the `ZIMIT_DEFINITION_VERSION` defined in `dev/docker-compose.yml`

- To register a worker
  ```sh
  dev/create_worker.sh
  ```

NOTE: These shell scripts have been configured withs some reasonable defaults like:

- admin username is `admin` with password `admin`. This must be the same as teh `INIT_USERNAME` AND `INIT_PASSWORD` of the `zimfarm-api` service and `_ZIMFARM_USERNAME` and `_ZIMFARM_PASSWORD` of the `zimit-api` service. See the Compose file for the definition of these environment variables.
- a worker `test_worker` with 1Gb memory, 1Gb disk and 1 CPU. These are specified in the `environment` section of the `zimfarm-worker-manager` too.

If you have requested a task via Zimit UI and want to simulate a worker starting this task to observe the consequence in Zimit UI, you might use the `dev/start_first_req_task.sh`.

## Restart the backend

Should the API process fail, you might restart it with:

```sh
docker restart zimit-zimit_api-1
```

## Browse the web UIs

You might open following URLs in your favorite browser:

- [Zimit UI Prod](http://localhost:8000)
- [Zimit UI Dev](http://localhost:8001)
- [Zimit API](http://localhost:8002)
- [Zimfarm UI](http://localhost:8003)
- [Zimfarm API](http://localhost:8004)

You can login into Zimfarm UI with username `admin` and password `admin`.
