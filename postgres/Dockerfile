FROM postgres:13

# Install required packages including git
RUN apt-get update && \
    apt-get install -y postgresql-server-dev-13 gcc make git && \
    git clone --branch v0.2.0 --single-branch https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install && \
    cd .. && \
    rm -rf pgvector && \
    apt-get remove --purge -y postgresql-server-dev-13 gcc make git && \
    apt-get autoremove -y && \
    apt-get clean
# Copy initialization script if needed
COPY init.sql /docker-entrypoint-initdb.d/
