# Pytch

Pytch is an innovative open-source platform designed to revolutionize the world of soccer analytics. Developed at Texas A&M University's Department of Computer Science and Engineering, this project utilizes state-of-the-art machine learning and computer vision techniques to offer accessible, in-depth soccer match analysis to fans, analysts, and enthusiasts.

## Features

- **Analytics**: Pytch provides a range of soccer analytics including shotmaps, heatmaps, and passmaps.
- **User Uploads**: Users can upload soccer footage to receive detailed analytics.
- **Custom Visualizations**: Supports custom visualizations, allowing users to tailor their analytics experience.
- **Open-Source**: Encourages community collaboration and innovation.

## Getting Started

### Prerequisites

- Ensure you have [Python](https://www.python.org/downloads/) and [Node.js](https://nodejs.org/en/download/) installed on your machine.
- Basic knowledge of machine learning and computer vision concepts is beneficial.

### frontend setup

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

### backend setup

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


## Project Structure
- `db/`: Contains database-related configurations and files.
- `docs/`: Includes comprehensive documentation for the project.
- `frontend/`: Houses the front-end code of the application.
- `tracker/`: contains Yolov8 identification, ByteTrack, Team Detection, and Localization start with :`flask --app app run -p 8080`

## Contributing
Contributions are what make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
1. Create your Feature Branch (git checkout -b feature/AmazingFeature)
1. Commit your Changes (git commit -m 'Add some AmazingFeature')
1. Push to the Branch (git push origin feature/AmazingFeature)
1. Open a Pull Request

## Team

- Gabriel Diaz - Computer Vision Engineer
- Ryan Kutz - Computer Vision Engineer
- Anthony Pasala - Backend Engineer
- Joseph Quismorio - Frontend Development Head
- Ryan Son - Project Manager
- Shurui Xu - Database and Analytics Engineer
