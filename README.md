# top-voted-devQnA
When learning new topics in computer programming, you might want to
know the top highest voted questions on Stack Overflow with a specific
keyword. This project helps you to that by showing the top highest
voted questions of a keyword with the highest voted answer on the site.

## Project files
The project includes three files:
1. `stackoverflow.py` is the main script.
2. `utils.py` is where you build core functions.
3. `README.md` is where you provide information about other files.

## How to run
- Required flags:
   * `question_number` is number of the top highest questions
   * `label` is the keyword
- A sample command:
   * `python3 stackoverflow.py --question_number 10 --label sql`
- A sample output of
`python3 stackoverflow.py --question_number 5 --label git` <br>
![sample_output](./sample_output.png "sample output")

