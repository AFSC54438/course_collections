import requests
from cs50 import get_string
import json
from termcolor import colored

BASE = "http://127.0.0.1:5000/igcse"

subj_codes = []
while True:
    subj = get_string("Enter subj code: ")

    if subj == "":
        break

    subj_codes.append(subj)

args = "&subjs=".join(subj_codes)

print(colored(f"{BASE}?subjs={args}", "blue"))
response = requests.get(f"{BASE}?subjs={args}")

data_dict = ""
if response.status_code == 200:
    data_dict = json.loads(response.text)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

print(data_dict)