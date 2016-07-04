
import core
from docopt import docopt

command_line = """Solaris Manager

Usage:
    solaris run
    solaris rm

Options:
    -h help     show this screen
"""


def main():
    arguments = docopt(command_line)
    if arguments['run']:
        core.run()
    elif arguments['rm']:
        core.remove()
    else:
        print "Error: No instruction passed"

if __name__ == '__main__':
    main()
