FROM mcr.microsoft.com/mssql/server:2022-latest

ARG PASSWORD

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=${PASSWORD}

USER root

COPY db/ /

RUN chmod +x /import_data.sh

CMD /bin/bash ./entrypoint.sh