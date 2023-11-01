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
