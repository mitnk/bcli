

def get_info(args):
    with open('./sessions/latest/deploy.json') as f:
        print(f.read())
