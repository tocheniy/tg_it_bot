import sys

sys.path.append(".")
# print(sys.path)
from arq import run_worker
from work_settings import WorkerSettings
# import logging

# worker = WorkerSettings()


def main():
    run_worker(WorkerSettings)
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)


if __name__ == "__main__":
    main()
