# Docker Redis Counter

A small Python web app that counts page visits. The counter is stored in
Redis, and both services run as containers with Docker Compose.

## Architecture

```
Browser -> web (Python, :5000) -> redis (:6379) -> volume redis-data
```

## Run it

```bash
git clone git@github.com:AhmedSakr9/docker-redis-counter.git
cd docker-redis-counter
docker compose up -d --build
curl localhost:5000
```

Stop: `docker compose down` (data kept) or `docker compose down -v` (data deleted).

## What I learned
- Images vs containers, layers, and build caching
- Services reach each other by name on the Compose network
- Volumes keep data after containers are removed

## Problems I hit and how I fixed them
| Problem | Cause | Fix |
|---------|-------|-----|
| Empty reply from server | Wrong `REDIS_HOST` | Read the last line of the traceback, fixed the hostname |
| Name resolution error | Redis container was stopped | `docker compose start redis` |
| Port already allocated | Another container held port 5000 | Found it with `docker ps`, removed it |
| Build failed | Typo in `COPY` | Read the failing step number, fixed the filename |
| Restarting container | Bad command plus restart policy | Read the logs, removed the override |
| Git permission errors | Ran `git` with `sudo` | `chown` the folder back to my user |

## Next improvements
Healthchecks, non-root user, CI with GitHub Actions.
