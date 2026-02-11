# InazumaAPI

An API for the first game in the Inazuma Eleven series.

## Documentation

You can access the docs [here](https://inazumaelevenapi.onrender.com/docs).

## Building from Source

You can build the API yourself using **Docker**.

Build the image and then run it:

```sh
docker build -t inazuma-eleven-api:latest .
docker run -p 8000:8000 --name inazuma-api inazuma-eleven-api:latest
```

Or use **Docker Compose**:

```sh
docker compose up
```
