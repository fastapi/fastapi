# FastAPI Project - Deployment

You can deploy the using Docker Compose with a main Traefik proxy outside handling communication to the outside world and HTTPS certificates.

And you can use CI (continuous integration) systems to do it automatically.

But you have to configure a couple things first.

## Traefik network

This stack expects the public Traefik network to be named `traefik-public`.

If you need to use a different Traefik public network name, update it in the `docker-compose.yml` files, in the section:

```YAML
networks:
  traefik-public:
    external: true
```

Change `traefik-public` to the name of the used Traefik network. And then update it in the file `.env`:

```bash
TRAEFIK_PUBLIC_NETWORK=traefik-public
```
