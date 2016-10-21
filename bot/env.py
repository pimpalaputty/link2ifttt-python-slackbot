import os
import logging
import ast

# log_level = os.getenv("LOG_LEVEL", "INFO")
log_level = "INFO"
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

URL_BLACKLIST = ast.literal_eval(os.getenv("URL_BLACKLIST", ""))
logging.info("URL_BLACKLIST: {}".format(URL_BLACKLIST))

SLACK_TOKEN = os.getenv("SLACK_TOKEN", "")
logging.info("SLACK_TOKEN: {}".format(SLACK_TOKEN))

IFTTT_TOKEN = os.getenv("IFTTT_TOKEN", "")
logging.info("IFTTT_TOKEN: {}".format(IFTTT_TOKEN))

IFTTT_EVENT = os.getenv("IFTTT_EVENT", "")
logging.info("IFTTT_EVENT: {}".format(IFTTT_EVENT))

ALGO_TOKEN = os.getenv("ALGO_TOKEN", "")
logging.info("ALGO_TOKEN: {}".format(ALGO_TOKEN))