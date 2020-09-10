#!/usr/bin/env python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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


class CoffeeBot:
    def __init__(self, config):
        self.recipients = config["recipients"]
        self.sender_account = config["sender_account"]
        self.sender_password = config["sender_password"]
        self.sender_username = config["sender_username"]
        self.smtp_port = config["smtp_port"]
        self.smtp_server = config["smtp_server"]
        self.round = config["round"]

    def _make_pairs(self):
        hs = len(self.recipients) // 2
        fixed, moving = self.recipients[-1], self.recipients[:-1]
        current_rotation = moving[self.round:] + moving[:self.round]
        side_a, side_b = current_rotation[:hs], current_rotation[hs:]
        side_b = side_b[::-1] + [fixed]
        for a, b in zip(side_a, side_b):
            yield(a, b)


if __name__ == '__main__':
    main()
