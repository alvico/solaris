Solaris
========================

This project aims to add a set of tools enabling a solr developer or tester to run and deploy easily and transparent through docker an instance of solr.
Prerequisites:
    Python 2.7 
    docker

- Copy in a local folder the solr configuration and core details you wish to expose (solr.xml, core: conf/solrconf.xml and conf/schema.xml & index data)
- Set up the conf.py file according your needs in solaris/src/conf.py
- Install requisites.txt, preferable in a virtualenv.

The only supported method currently is to run a solr instance out of a pre made WAR, that should be placed in the shared_dir.

- Run: python core.py

You can now visit your solr instance in http://<docker-ip>:<Port>/trovit_solr
