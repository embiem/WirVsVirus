# Backend API

## Getting started

First run docker compose in parent directory

``` sh
docker-compose up -d
```

This should start the api in reload mode.  Any changes to code will reload the
api.

To follow logs:

``` sh
docker-compose logs -f
```

## Testing

To run tests

``` sh
docker-compose exec backend pytest
```

## Debugging

To debug, place a debug point somewhere in your code:

``` python
a = 3
print('before')
breakpoint()  # add this line
print('after')
```

attach to the docker image:

``` sh
docker attach wirvsvirus_backend_1
```

now you should be in the debugger in the docker container.
