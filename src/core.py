# -*- coding: utf-8 -*-
import docker
import helpers
import os.path

from pprint import pprint
from conf import config as CONF


def getDockerFile(path):
    return os.path.realpath('.').replace('/src', '') + path


def full(img='solr4'):
    solr_path = CONF['shared_dir'] + CONF['solr_dir']
    fpath = getDockerFile('/conf/solr4')
    client = docker.from_env(assert_hostname=False)
    response = [l for l in client.build(fpath, tag=img)]
    pprint(response)
    container = client.create_container(
        image=img,
        name='solr',
        volumes=['/opt/solr'],
        host_config=client.create_host_config(binds={
            solr_path: {
                'bind': '/opt/solr',
                'mode': 'rw',
                }}))
    pprint(container['Id'])
    status = client.start(container['Id'])
    pprint(status)
    # client.delete(container['Id'])


def from_war(img='solr4min', name='min'):
    docker_path = '/usr/local/deploys'
    f_path = getDockerFile('/conf/solr4-min')
    client = docker.from_env(assert_hostname=False)
    response = [l for l in client.build(f_path, tag=img)]
    pprint(response)
    container = dict()
    if CONF['port_forwarding']:
        container = client.create_container(
            image=img,
            name=name,
            ports=[8080],
            volumes=[docker_path],
            host_config=client.create_host_config(binds={
                CONF['shared_dir']: {
                    'bind': docker_path,
                    'mode': 'rw',
                    }},
                port_bindings={
                    8080: CONF['tomcat_port']
            }))
    else:
        container = client.create_container(
            image=img,
            name=name,
            ports=[8080],
            volumes=[docker_path],
            host_config=client.create_host_config(binds={
                CONF['shared_dir']: {
                    'bind': docker_path,
                    'mode': 'rw',
                    }}))
    pprint(container['Id'])
    pprint(client.start(container['Id']))


def set_up_solr(container='min'):
    def d_exec(cmd):
        return helpers.docker_exec(cmd, container)
    docker_path = '/usr/local/deploys'
    tomcat = '/usr/local/tomcat/webapps/'
    cp = "cp "
    cmd = cp + docker_path + "/trovit_solr.war " + tomcat
    pprint(cmd)
    d_exec(cmd)
    cmd = cp + " -r " + docker_path + "/solr " + "/var/local"
    pprint(cmd)
    d_exec(cmd)
    cmd = "cat /usr/local/tomcat/bin/catalina.sh"
    out, err = d_exec(cmd)
    line = 'JAVA_OPTS="$JAVA_OPTS -Xmx8G -Dsolr.solr.home=/var/local/solr/ '\
        '-Dsolr.data.dir=/var/local/solr/"'
    anchor = 'PRGDIR='
    content = helpers.insert_line_after(out.split('\n'), line, anchor)
    with open(CONF['shared_dir']+"tmp.txt", "w") as text_file:
        text_file.write('\n'.join(content))
    cat = "/usr/local/tomcat/bin/catalina.sh"
    cmd = "cp {0} {0}.bck".format(cat)
    d_exec(cmd)
    cmd = "{0}{1}/tmp.txt {2}".format(cp, docker_path, cat)
    d_exec(cmd)


def solr_start(container='min'):
    cmd = 'catalina.sh start'
    helpers.docker_exec(cmd, container)

from_war()
set_up_solr()
solr_start()
