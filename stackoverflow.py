#!/usr/bin/env python3
import argparse
import requests
from top_voted_stackoverflow import top_questions, top_answer


parser = argparse.ArgumentParser()

parser.add_argument(
    '--question_number',
    type=int,
    help="The number of top voted questions"
)

parser.add_argument(
    '--label',
    type=str,
    help="A keyword or tag of questions on Stack Overflow"
)

args = parser.parse_args()

session = requests.Session()

url = 'https://api.stackexchange.com/2.2/questions'


def main():
    """
    Script takes the top ** N ** highest voted question of the tag ** LABEL **
    on stackoverflow.com.
    """

    label = args.label
    question_number = args.question_number
    print('Top {} voted questions with tag "{}"'.format(
        question_number, label))

    if question_number >= 300:
        print("only make 300 requests per day")
        return

    questions = top_questions(question_number, label, url, session)
    for title, question_id in questions:
        answer_id = top_answer(question_id, url, session)
        link_to_answer = 'https://stackoverflow.com/a/{}'.format(answer_id)
        print(title + "\n", "\tHighest voted answer:", link_to_answer)


if __name__ == "__main__":
    main()
