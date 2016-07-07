import commands

from docopt import docopt

command_line = """Solaris Manager

Usage:
    solaris run
    solaris rm
    solaris rst

Arguments:
    run     builds containers (Solr and Mysql)
    rm      removes containers
    rst     restarts solr through catalina start|stop

Options:
    -h help     show this screen
"""


def main():
    arguments = docopt(command_line)
    if arguments['run']:
        commands.run()
    elif arguments['rm']:
        commands.remove()
    elif arguments['rst']:
        commands.restart_solr()
    else:
        print "Error: No instruction passed"

if __name__ == '__main__':
    main()
