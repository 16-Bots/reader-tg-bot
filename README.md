# Introduction

Repository contains the source code of the telegram bot for reading a books. Now you can read
"The Master and Margarita" book, others will be added in the future.

- Available functions:
    - /beginning: go to the beginning of the book
    - /continue: continue reading
    - /bookmarks: show added bookmarks
    - /help: bot documentation
    - /goto: Go to custom page

# Prerequisites

Be sure you have the following installed on your development machine:

1. Python >= 3.9
2. Git
3. pip
4. Virtualenv

# Setup

To run this project in your development machine, follow these steps:

1. Create and activate a virtual environment with
   [virtualenv](https://virtualenv.pypa.io/) or
   [venv](https://docs.python.org/3/library/venv.html)

2. Clone this repo: `git clone <repo_url>`

3. Install dependencies: `pip install -r requirements.txt`

4. Create `.env` file following the example file `.env.example`

5. Run `bot.py` file