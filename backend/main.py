import questions.histoire
import questions.geography
import questions.arts
import time
import random

question_generators = [questions.arts]


def generate_random_question():
    generator = random.choice(question_generators)
    return generator.generate_random_question()


if __name__ == "__main__":
    while True:
        # try:
        q, a, r = generate_random_question()
        # except Exception as e:
        #     print("Erreur : ", e)
        #     continue
        print(q)
        print(a)
        print(r)
        answer = input("Answer: ")
        if answer == str(r):
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was {r}")
        time.sleep(1)
