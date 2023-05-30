FROM mcr.microsoft.com/mssql/server:2022-latest

ARG PASSWORD
ARG USER_ID

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=${PASSWORD}
ENV USER_ID=${USER_ID}

USER root

COPY db/ /

RUN chmod +x /import_data.sh

CMD /bin/bash ./entrypoint.sh