import fileinput
import itertools
import subprocess


def insert_line_file(file, new_line, anchor):
    insert = False
    for line in fileinput.input(file, inplace=1):
        if line.startswith(anchor):
            insert = True
        else:
            if insert:
                print new_line
            insert = False
        print line


def insert_line_after(content, new_line, anchor):
    i = 0
    new_content = []
    for line in content:
        i += 1
        if line.startswith(anchor):
            head = itertools.islice(content, i)
            tail = iter(())
            if len(content) > 1:
                tail = itertools.islice(content, i, len(content))
            new_content = list(head) + [new_line] + list(tail)
            break
    return new_content


def docker_exec(cmd, container, usr="root"):
    full_cmd = "docker exec --user {0} {1} {2}".format(usr, container, cmd)
    # subprocess.call(full_cmd, shell=True)
    p = subprocess.Popen(full_cmd, stdout=subprocess.PIPE, shell=True)
    return p.communicate()
