FROM mysql:latest
ARG pass

ENV MYSQL_ROOT_PASSWORD ${pass}

COPY init.sql /docker-entrypoint-initdb.d/
