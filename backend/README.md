# Backend API

## Getting started

First run docker compose in parent directory

``` sh
docker-compose up -d
```

This should start the api in reload mode.  Any changes to code will reload the
api.

## Testing locally

``` sh
docker-compose exec backend ...
pip install -e ".[dev]"
```


