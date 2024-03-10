from frontend.interface import app
import argparse

from threading import Timer
import webbrowser
import asyncio as aio


def open_browser():
    webbrowser.open_new("http://localhost:5000")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--console", action="store_true")
    args = parser.parse_args()
    if not args.console:
        Timer(1, open_browser).start()
        app.run(debug=args.debug)
    else:
        print("Console mode")
        from backend.main import run_in_console

        aio.run(run_in_console())
