FROM mcr.microsoft.com/mssql/server:2022-latest

USER root

COPY db/ /

RUN chmod +x /import_data.sh

CMD /bin/bash ./entrypoint.sh