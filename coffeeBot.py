#!/usr/bin/env python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import datetime


def main():

    with open("./config.json", 'r') as fin:
        config = json.load(fin)
    bot = CoffeeBot(config)
    bot._send_mails()
    # config["round"] = config["round"] % (len(config["email_recepients"]) - 1)
    # pairs_iter = make_pairs(
    #     config["round"], config["email_recepients"])
    # config["round"] += 1
    # with open("./config.json", 'w') as fout:
    #     json.dump(config, fout, indent=2, sort_keys=True)


class CoffeeBot:
    def __init__(self, config):
        year, week_num, day_of_week = datetime.date.today().isocalendar()
        self.subject = config["subject"] + " Week {} {}".format(year, week_num)
        self.recipients = config["recipients"]
        self.sender_account = config["sender_account"]
        self.sender_password = config["sender_password"]
        self.sender_username = config["sender_username"]
        self.smtp_port = config["smtp_port"]
        self.smtp_server = config["smtp_server"]
        self.round = config["round"]

    def _send_mails(self):
        server = smtplib.SMTP(self.smtp_server,self.smtp_port)
        server.starttls()
        server.login(self.sender_username, self.sender_password)
        for a, b in self._make_pairs():
            if a == "BREAK":
                continue
            elif b == "BREAK":
                continue
            else:
                message = MIMEMultipart('alternative')
                message['From'] = self.sender_account
                message['To'] = recipient
                message['Subject'] = self.subject
                message.attach(MIMEText(self.body, 'html'))
                text = message.as_string()
                server.sendmail(self.sender_account,recipient,text)#All emails sent, log out.
        server.quit()

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
