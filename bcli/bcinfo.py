import os

import bcutils


def get_info(args):
    if bcutils.no_sessions():
        print('no sessions, please deploy first')
        exit(1)

    with open(bcutils.get_deployed_info_file()) as f:
        print(f.read())
