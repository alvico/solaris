FROM	java:openjdk-6-jdk
MAINTAINER Albert Vico "albertvico@trovit.com"

# Should get the code from local repo/directory
# Do solr installing magic

ENV SOLR_USER solr
ENV SOLR_UID 8983

RUN apt-get update && apt-get install -y procps
RUN apt-get install -y maven

RUN groupadd -r -g $SOLR_UID $SOLR_USER && \
  useradd -r -u $SOLR_UID -g $SOLR_USER $SOLR_USER

RUN mkdir /docker-entrypoint-initdb.d /opt/docker-solr/
COPY scripts /opt/docker-solr/scripts
RUN chown -R $SOLR_USER:$SOLR_USER /opt/docker-solr
RUN chmod +x /opt/docker-solr/scripts/docker-entrypoint.sh
RUN chmod +x /opt/docker-solr/scripts/wait-for-solr.sh

ENV PATH /opt/solr/bin:/opt/docker-solr/scripts:$PATH

EXPOSE 8983
WORKDIR /opt/solr
USER $SOLR_USER

#ENTRYPOINT[docker-entrypoint.sh"]
#CMD ["solr"]
CMD ["/bin/ping","localhost"]
