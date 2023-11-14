# Project setup

## frontend setup

- `cd frontend`
- Fill out env vars: `cp .env.example .env`
- Install packages: `npm install` or `pnpm i`
- database setup
  - Have docker running
    - start server: `docker-compose up -d`
    - if you want to stop: `docker-compose down` or in the docker app
  - push schema to db server: `npx prisma db push` or `pnpm prisma db push`
  - view database: `npx prisma studio` or `pnpm prisma studio`

- start frontend: `npm run dev` or `pnpm dev`

## backend setup

- `pip install cython`
- `cd tracker/track`
- `python -m pip install --upgrade pip==22.0.4`
- `pip install -r requirements.txt`
- `rm -rf ByteTrack`
- `git clone git@github.com:ifzhang/ByteTrack.git --force`
- `cd ByteTrack`
- `pip install -r requirements.txt`
- `python setup.py develop`
- `cd ../..`
- `flask --app app run -p 8080`
