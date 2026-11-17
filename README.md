# Docker Redis Counter: Hands-On Lab

A hands-on containerization lab: a Python web app with a Redis backend,
orchestrated with Docker Compose, with persistent storage and documented
failure scenarios.

## Objective

Build and operate a multi-container application, and practice the
deployment and troubleshooting skills used in real DevOps work.

## Architecture

```
Browser -> web (Python, :5000) -> redis (:6379) -> volume redis-data
```

| Component | Role |
|-----------|------|
| `web` | Python HTTP server; increments a visit counter on each request |
| `redis` | Stores the counter (`redis:7-alpine`) |
| `redis-data` volume | Keeps data after containers are removed |
| Compose network | Lets `web` reach Redis by service name |

## Environment

- Host: Windows, VirtualBox
- Guest: Ubuntu Server VM, accessed over SSH
- Docker Engine and Docker Compose v2

## Run it

```bash
git clone git@github.com:AhmedSakr9/docker-redis-counter.git
cd docker-redis-counter
docker compose up -d --build
curl localhost:5000
```

Stop: `docker compose down` (data kept) or `docker compose down -v` (data deleted).

## Lab exercises

**1. Persistence test**
Ran `docker compose down` then `up`: the counter continued.
Ran `docker compose down -v`: the counter reset to 1.
Result: containers are disposable, volumes hold the data.

**2. Failure scenarios**

| Scenario | Symptom | Root cause | Diagnosis | Fix |
|----------|---------|------------|-----------|-----|
| Wrong Redis hostname | `Empty reply from server` | `REDIS_HOST` pointed to a name that does not exist | Last line of the traceback in `docker compose logs web` | Corrected the variable |
| Redis stopped | Same symptom; DNS error for `redis` | Docker DNS only resolves running containers | `docker compose ps` showed no `redis` | `docker compose start redis` |
| Port conflict | `port is already allocated` | Another container held port 5000 | `docker ps` PORTS column | Removed the blocking container |

**3. Git and access issues**

| Issue | Cause | Fix |
|-------|-------|-----|
| `Repository not found` | Wrong username in the remote URL | Found the real one with `ssh -T git@github.com` |
| Permission errors in `.git` | Ran `git` with `sudo` | `chown -R` back to my user; never use `sudo` with Git |

## Key takeaways

- A running container does not mean a working app: check `ps`, then logs.
- Read tracebacks from the bottom line up.
- Services find each other by name on the Compose network.
- Pin image versions and keep secrets out of Git.

## Roadmap

- [x] Healthchecks
- [x] Non-root container user
- [x] `.env` configuration
- [ ] CI with GitHub Actions (build on every push)
