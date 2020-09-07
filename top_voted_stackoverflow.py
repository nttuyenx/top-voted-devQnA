import argparse
import requests
import html

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


class QuotaOverflow(Exception):
    """
    Raise exception if the question_number is greater than 300.
    """
    pass


def get_pagesizes_range(number):
    """
    Get page sizes range.

    :param number: the number of top voted questions
    :type number: int
    :return: the list of page sizes
    :rtype: list

    """

    result = []
    for _ in range(number // 100):
        result.append(100)
    if number % 100 != 0:
        result.append(number % 100)
    return result


def top_questions(number, label):
    """
    Get titles and question ids of top voted questions, which are
    tagged with a keyword on Stack Overflow.

    :param number: the number of top voted questions
    :type number: int
    :param label: the tagged keyword of questions
    :type label: str
    :return: the list of pairs of title and question id
    :rtype: list
    """

    pagesizes = get_pagesizes_range(number)
    try:
        top_ques = []
        for page, pagesize in enumerate(pagesizes, 1):
            params = {"page": page,
                      "pagesize": pagesize,
                      "order": "desc",
                      "sort": "votes",
                      "tagged": label,
                      "site": "stackoverflow"}
            resp = session.get(url, params=params).json()["items"]
            for item in resp:
                title = html.unescape(item["title"])
                question_id = item['question_id']
                top_ques.append((title, question_id))
        return top_ques
    except Exception:
        raise QuotaOverflow("only make 300 requests per day")


def top_answer(question_id):
    """
    Get the answer id of the highest voted answer of the question.

    :param question_id: question id
    :type question_id: str
    :return: answer id of the highest voted answer
    :rtype: str
    """

    link = '{}/{}/answers'.format(url, question_id)
    params = {"pagesize": 1,
              "order": "desc",
              "sort": "votes",
              "site": "stackoverflow"}
    try:
        resp = session.get(link, params=params).json()["items"]
        answer = resp[0]['answer_id']
        return answer
    except Exception:
        raise QuotaOverflow("only make 300 requests per day")


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

    questions = top_questions(question_number, label)
    for title, question_id in questions:
        answer_id = top_answer(question_id)
        link_to_answer = 'https://stackoverflow.com/a/{}'.format(answer_id)
        print(title + "\n", "\tHighest voted answer:", link_to_answer)


if __name__ == "__main__":
    main()
