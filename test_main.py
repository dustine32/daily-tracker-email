import argparse

parser = argparse.ArgumentParser()
parser.add_argument('repo_name')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args.repo_name)