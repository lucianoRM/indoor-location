import multiprocessing as mp
import sys

from api import create_app, ENABLE_LOG_ARG
from src.gui.app import App

def run_server(enable_log):
    api = create_app(enable_log)
    api.run(host="0.0.0.0", port=8082, debug=False, use_reloader=False)

if __name__ == '__main__':
    enable_log = False
    if (len(sys.argv) > 1):
        if (ENABLE_LOG_ARG in sys.argv):
            enable_log = True

    p = mp.Process(target=run_server, args=(enable_log,))
    p.start()
    app = App(name="Indoor Location")
    event = mp.Event()

    def stop_server():
        p.terminate()
        event.set()

    app.on_stop(stop_server)
    app.start()

    p.join()



