# coffeeBuddyBot

The coffeeBuddyBot is an email bot. It uses an [Round Robin](algorithm) to pair
up people in a social group and notify each member about their current pairing
by mail. Useful for setting up weekly 1-on-1 coffee meetings in a research group.


## Usage

First clone this repo:

```
git clone https://github.com/nickmachnik/coffeBuddyBot.git [TARGET DIR]
```

Then you will need to set up the configuration of the bot, i.e. the mail
credentials of the bot and the contacts of the people in the social group.
The format is specified in `config_example.json`.

Simply copy this file to the directory your `coffeeBot.py` is in, name it
`config.json`, fill it out, and you are ready to go!


## License

MIT license ([LICENSE](LICENSE.txt) or https://opensource.org/licenses/MIT)