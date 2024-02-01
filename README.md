# gingko-take-home

A full-stack web app that can determine whether a particular DNA strand (user-provided) encodes a portion of a genome in a well-known set.

# Local development instructions

1. Clone the repo
2. Copy `deploy/docker/docker-compose-dev.yml` to the root directory to override `docker-compose.yml`
3. Run `docker-compose up -d --build` to build the containers and run in detached mode
4. Navigate to `http://localhost:3000` to view the frontend.

# If I had more time...

If I had more time, I would:

- add unit tests!
- spend more time on the security of the production deployment
- add some authentication
- make the frontend look a little nicer
