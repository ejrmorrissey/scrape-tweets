import multiprocessing
import time
import requests
import sys

from main import app


def main_loop():
    response = None
    while response is None or response.status_code != 200:
        try:
            response = requests.get(f"http://0.0.0.0:5000/")
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    requests.get(f"http://0.0.0.0:5000/loadTimeline")
    while True:
        time.sleep(60*10)
        requests.get(f"http://0.0.0.0:5000/updateTimeline")


if __name__ == "__main__":
    p = multiprocessing.Process(target=main_loop)
    p.start()
    app.config['handle'] = sys.argv[2]
    app.run(use_reloader=False, host='0.0.0.0', debug=False)
    p.join()
