# goobta.io

Personal website frontend — a static [Astro](https://astro.build) site, served as
static files behind the `deploy-goobta.io` orchestration stack.

## Develop

```bash
npm install
npm run dev        # http://localhost:4321 with hot reload
```

## Build

```bash
npm run build      # static output -> dist/
npm run preview    # preview the built site locally
```

## Docker

Multi-stage build (Node build stage -> nginx serving static files on port 80):

```bash
docker build -t goobta-site .
docker run --rm -p 8080:80 goobta-site   # http://localhost:8080
```

## Deploy

Pushing to `main` triggers CI (`.github/workflows/build.yml`) to build and push
`ghcr.io/goobta/site:latest` (and `:<sha>`) to the GitHub Container Registry. The
`deploy-goobta.io` orchestration repo pulls that image and serves it at `goobta.io`
through its Caddy reverse proxy.

## Structure

```
src/
  layouts/Base.astro   shared document shell + global styles
  pages/index.astro    the home page
public/                static assets served as-is (favicon, etc.)
Dockerfile             build stage -> nginx serve stage
nginx.conf             static serving config
```

## Adding React later

```bash
npx astro add react
```

Then drop React components into pages with a client directive (e.g. `client:load`)
where you need interactivity. Static pages stay zero-JS.
