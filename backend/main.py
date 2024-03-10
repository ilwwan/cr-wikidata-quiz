from .questions import generate_random_question
import time
import argparse
import asyncio as aio


async def run_in_console():
    while True:
        # try:
        q, a, r = await generate_random_question()
        # except Exception as e:
        #     print("Erreur : ", e)
        #     continue
        print(q)
        print(a)
        answer = input("Answer: ")
        if answer == str(r):
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was {r}")
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--console", action="store_true")
    parser.add_argument("--length", type=int, default=5)
    args = parser.parse_args()
    if args.console:
        print("Console mode")
        aio.run(run_in_console())
