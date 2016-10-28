#!/usr/bin/env python

import logging
import os
import env

from beepboop import resourcer
from beepboop import bot_manager

from slack_bot import SlackBot
from slack_bot import spawn_bot

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

    if env.SLACK_TOKEN == "":
        logging.info("SLACK_TOKEN env var not set, expecting token to be provided by Resourcer events")
        env.SLACK_TOKEN = None
        botManager = bot_manager.BotManager(spawn_bot)
        res = resourcer.Resourcer(botManager)
        res.start()
    elif env.IFTTT_TOKEN == "":
        logging.info("IFTTT_TOKEN env var not set, expecting token to be provided by Resourcer events")
        env.IFTTT_TOKEN = None
        botManager = bot_manager.BotManager(spawn_bot)
        res = resourcer.Resourcer(botManager)
        res.start()
    elif env.IFTTT_EVENT == "":
        logging.info("IFTTT_EVENT env var not set, expecting token to be provided by Resourcer events")
        env.IFTTT_EVENT = None
        botManager = bot_manager.BotManager(spawn_bot)
        res = resourcer.Resourcer(botManager)
        res.start()
    else:
        # only want to run a single instance of the bot in dev mode
        bot = SlackBot(env.SLACK_TOKEN)
        bot.start({})
