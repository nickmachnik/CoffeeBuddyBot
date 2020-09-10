#!/usr/bin/env python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import datetime


def main():

    with open("./config.json", 'r') as fin:
        config = json.load(fin)
    config["round"] = config["round"] % (len(config["recipients"]) - 1)
    bot = CoffeeBot(config)
    bot._send_test("nick.machnik@gmail.com")
    bot._send_test("nick.machnik@ist.ac.at")
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
        year, week_num, day_of_week = datetime.date.today().isocalendar()
        self.subject = config["subject"] + " Week {} {}".format(week_num, year)

    def _send_test(self, recipient):
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.sender_username, self.sender_password)
        message = MIMEMultipart('alternative')
        message['From'] = self.sender_account
        message['To'] = recipient
        message['Subject'] = self.subject
        body = "This is a coffee buddy bot test mail."
        message.attach(MIMEText(body, 'html'))
        text = message.as_string()
        server.sendmail(self.sender_account, recipient, text)
        server.quit()

    def _send_mails(self):
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.sender_username, self.sender_password)
        for a, b in self._make_pairs():
            if a == "BREAK":
                self._send_break_message(server, b)
            elif b == "BREAK":
                self._send_break_message(server, a)
            else:
                self._send_buddy_message(server, a, b)
                self._send_buddy_message(server, b, a)
        server.quit()

    def _send_buddy_message(self, server, recipient, buddy):
        message = MIMEMultipart('alternative')
        message['From'] = self.sender_account
        message['To'] = recipient
        message['Subject'] = self.subject
        body = "Your coffee body this week is {}".format(buddy)
        message.attach(MIMEText(body, 'html'))
        text = message.as_string()
        server.sendmail(self.sender_account, recipient, text)

    def _send_break_message(self, server, recipient):
        message = MIMEMultipart('alternative')
        message['From'] = self.sender_account
        message['To'] = recipient
        message['Subject'] = self.subject
        body = "You have a break from coffee buddies this week :)"
        message.attach(MIMEText(body, 'html'))
        text = message.as_string()
        server.sendmail(self.sender_account, recipient, text)

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
