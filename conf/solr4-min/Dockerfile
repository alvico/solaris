FROM	tomcat:6.0.45-jre7
MAINTAINER Albert Vico "albertvico@trovit.com"

# Should get the code from local repo/directory
# Do solr installing magic

ENV SOLR_USER solr
ENV SOLR_UID 8983

RUN groupadd -r -g $SOLR_UID $SOLR_USER && \
  useradd -r -u $SOLR_UID -g $SOLR_USER $SOLR_USER

EXPOSE 8080:8080

#CMD ["solr"]
#CMD ["catalina.sh","run"]
CMD ["/bin/ping","localhost"]
