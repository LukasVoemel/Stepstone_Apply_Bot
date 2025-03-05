# Stepstone_Apply_Bot

With this tool you can easily automate the process of applying for jobs on Stepstone.de!

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. Install selenium. I used `pip3` to install the selenium package.

`pip3 install selenium`

### Usage

- Update your **username/email** and **password** in the `get_stepstone_cookies.py` and `stepstone_search.py` files.
- The `get_stepstone_cookies.py` script saves your session cookies to a pickle file, allowing you to stay logged in during the session.
- In `stepstone_search.py`, modify the **job title** and **location** in the main execution block.
- Applied jobs are logged in a text file for reference.
- The bot can attempt applications for all job listings retrieved from the search

### How to Run

Run `get_stepstone_cookies.py` to get session cookies.
Run `stepstone_search.py` to start appling.
