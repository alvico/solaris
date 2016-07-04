"""
.. module:: conf.
    :synopsis: Config file to be used with the module
.. moduleauthor:: Albert Vico
"""

config = {
    # path to dir that will be mounted in docker
    'shared_dir': '/path/to/some/dir',
    # relative path to solr conf and index files in shared_dir
    'solr_dir': 'solr4/',
    # Forwarding rnsblrf, msnfsyoty in OSX
    'port_forwarding': 'True',
    # Port that will be exposed in host
    'tomcat_port': '8080',
    # Pass for Mysql
    'mysqlpass': 'pass'
}
