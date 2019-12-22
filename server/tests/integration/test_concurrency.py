from threading import Thread
import multiprocessing as mp
from time import sleep

import requests
from pytest import fixture

from api import ANCHORS_ENDPOINT, create_app

class TestConcurrency:


    def __run_server(self):
        api = create_app(False)
        api.run(host="0.0.0.0", port=8082, debug=True, use_reloader=False, threaded=True)


    @fixture(autouse=True)
    def set_up(self):
        p = mp.Process(target=self.__run_server)
        p.start()
        print("STARTED")
        yield p
        p.terminate()
        p.join()
        print("TERMINATED")


    def test_requests_are_excuted_in_parallel(self):
        sleep(2)
        anchors = []
        def add_id(id):
            anchor = {
                "id": str(i),
                "position": {
                    'x': 0,
                    'y': 0,
                }
            }
            requests.post("http://localhost:8082" + ANCHORS_ENDPOINT, json=anchor)
            a = requests.get("http://localhost:8082" + ANCHORS_ENDPOINT + "/" + str(id))
            anchors.append(a.json()['id'])

        for i in range(200):
            Thread(target=add_id, args=(i,)).run()

        for i in range(200):
            assert anchors[i] == str(i)

