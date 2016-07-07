import core
import docker
import helpers
import time

from pprint import pprint


def remove():
    client = docker.from_env(assert_hostname=False)
    flag = 0
    if client.containers(filters={'name': 'min'}):
        client.remove_container('min', force=True)
        flag = 1
    if client.containers(filters={'name': 'mysql'}, all=True):
        client.remove_container('mysql', force=True)
        flag = flag + 2

    if flag == 1:
        pprint("Solr min container removed")
    elif flag == 2:
        pprint("Mysql container removed")
    elif flag == 3:
        pprint("Solr and Mysql containers removed")
    else:
        pprint("nothing to remove")


def run():
    core.create_mysql()
    core.from_war()
    core.set_up_solr()
    core.solr_start()


def restart_solr():
    client = docker.from_env(assert_hostname=False)
    if client.containers(filters={'name': 'min'}):
        helpers.docker_exec("catalina.sh stop", "min")
        time.sleep(5)
        helpers.docker_exec("catalina.sh start", "min")
        pprint('Solr restarted')
    else:
        pprint('Solr not running')
