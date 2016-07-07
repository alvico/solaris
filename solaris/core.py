# -*- coding: utf-8 -*-
import docker
import helpers
import os.path
import time

from pprint import pprint
from conf_local import config as CONF

DOCKER_PATH = '/usr/local/deploys'


def getDockerFile(path):
    tmp = os.path.relpath(__file__)
    head, tail = os.path.split(tmp)
    dpath = head + path
    return dpath


def from_war(img='solr4min', name='min'):
    f_path = getDockerFile('/assets/solr4-min')
    client = docker.from_env(assert_hostname=False)
    response = [l for l in client.build(f_path, tag=img)]
    pprint(response)
    container = dict()
    if CONF['port_forwarding']:
        container = client.create_container(
            image=img,
            name=name,
            ports=[8080],
            volumes=[DOCKER_PATH],
            host_config=client.create_host_config(binds={
                CONF['shared_dir']: {
                    'bind': DOCKER_PATH,
                    'mode': 'rw',
                    }},
                port_bindings={
                    8080: CONF['tomcat_port']
            }))
    else:
        container = client.create_container(
            image=img,
            name=name,
            volumes=[DOCKER_PATH],
            host_config=client.create_host_config(binds={
                CONF['shared_dir']: {
                    'bind': DOCKER_PATH,
                    'mode': 'rw',
                    }}))
    pprint(container['Id'])
    client.start(container['Id'])


def set_up_solr(container='min'):
    def d_exec(cmd):
        return helpers.docker_exec(cmd, container)
    tomcat = '/usr/local/tomcat/webapps/'
    cp = "cp "
    cmd = cp + DOCKER_PATH + "/trovit_solr.war " + tomcat
    pprint(cmd)
    d_exec(cmd)
    cmd = cp + " -r " + DOCKER_PATH + "/solr " + "/var/local"
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
    cmd = "{0}{1}/tmp.txt {2}".format(cp, DOCKER_PATH, cat)
    d_exec(cmd)


def solr_start(container='min'):
    cmd = 'catalina.sh start'
    helpers.docker_exec(cmd, container)
    client = docker.from_env(assert_hostname=False)
    # TODO: only works with one bridge network
    net = client.networks(names=['bridge'])[0]
    cont = net['Containers']
    ip = [c['IPv4Address'] for c in cont.values() if c['Name'] == 'mysql']
    if ip:
        ip = ip[0].split('/')[0]
        h1 = "slave.solr.global.mysql"
        h2 = "slave.homes.es.ppc.mysql"
        h3 = "slave.pipeline.mysql"
        h4 = "master.homes.es.ppc.mysql"
        tab = "\t"
        line = "{0}{1}{2} {3} {4} {5}".format(ip, tab, h1, h2, h3, h4)
        out, err = helpers.docker_exec("cat /etc/hosts", container)
        out = out.split('\n')
        anch = out[-1]
        content = helpers.insert_line_after(out, line.replace('\n', ''), anch)
        with open(CONF['shared_dir']+"tmp1.txt", "w") as text_file:
            text_file.write('\n'.join(content))
        hosts = "/etc/hosts"
        cmd = "cp {0}/tmp1.txt {1}".format(DOCKER_PATH, hosts)
        helpers.docker_exec(cmd, container)
    else:
        print "Mysql Container not working"


def create_mysql():
    def d_exec(cmd):
        return helpers.docker_exec(cmd, 'mysql')
    f_path = getDockerFile('/assets/mysql')
    client = docker.from_env(assert_hostname=False)
    response = [l for l in client.build(f_path, tag='mysql')]
    pprint(response)
    enviro = ["MYSQL_ROOT_PASSWORD="+CONF["mysqlpass"]]
    container = client.create_container(
        image='mysql',
        name='mysql',
        environment=enviro,
        volumes=[DOCKER_PATH],
        host_config=client.create_host_config(binds={
            CONF['shared_dir']: {
                'bind': DOCKER_PATH,
                'mode': 'rw',
            }}))
    pprint(container['Id'])
    client.start(container['Id'])
    time.sleep(2)
    cmd = "cp /usr/local/deploys/{0}".format(CONF['mysqldump'])
    cmd = cmd + ' /docker-entrypoint-initdb.d'
    print cmd
    d_exec(cmd)
