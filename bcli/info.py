from bcli import utils


def get_info(args):
    if utils.no_sessions():
        print('no sessions, please deploy first')
        exit(1)

    with open(utils.get_deployed_info_file()) as f:
        print(f.read())
