import os

import bcutils


def get_info(args):
    file_deployed_info = bcutils.get_deployed_info_file()
    if not os.path.exists(file_deployed_info):
        print('deployed info file not found')
        exit(1)

    with open(file_deployed_info) as f:
        print(f.read())
