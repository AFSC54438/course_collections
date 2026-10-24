import requests
from cs50 import get_string, get_int
import json
from termcolor import colored

BASE = "https://cies-ugfb.onrender.com/"

print("Levels:")
print("1) IGCSE")
print("2) A Level")

level = ""
while level not in [1, 2, 3]:
    level = get_int("Which level (1/2)? ")

new_base = BASE

if level == 1:
    new_base += "igcse"
elif level == 2:
    new_base += "a_lvl"


subj_codes = []
while True:
    subj = get_string("Enter subj code: ")

    if subj == "":
        break

    subj_codes.append(subj)

args = "&subjs=".join(subj_codes)

print(colored(f"{new_base}?subjs={args}", "blue"))
response = requests.get(f"{new_base}?subjs={args}")

data_dict = ""
if response.status_code == 200:
    data_dict = json.loads(response.text)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

print(data_dict)