#!/usr/bin/env python

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
import json


def main():
    with open("./config.json", 'r') as fin:
        config = json.load(fin)
    config["round"] = config["round"] % (len(config["email_recepients"]) - 1)
    pairs_iter = make_pairs(
        config["round"], config["email_recepients"])
    config["round"] += 1
    with open("./config.json", 'w') as fout:
        json.dump(config, fout, indent=2, sort_keys=True)


def make_pairs(i, people):
    hs = len(people) // 2
    fixed, moving = people[-1], people[:-1]
    current_rotation = moving[i:] + moving[:i]
    side_a, side_b = current_rotation[:hs], current_rotation[hs:]
    side_b = side_b[::-1] + [fixed]
    for a, b in zip(side_a, side_b):
        yield(a, b)


if __name__ == '__main__':
    main()
