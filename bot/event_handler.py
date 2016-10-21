import json
import logging
import re
import requests
import Algorithmia
import env

logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            # self.msg_writer.write_help_message(event['channel'])
            pass
        elif event_type == 'group_joined':
            # you joined a private group
            # self.msg_writer.write_help_message(event['channel'])
            pass
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself, and from non-users (eg. webhooks)
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):
            logger.debug(u'Received event: {}'.format(event))
            
            msg_txt = event['text'].lower()

            re_pattern = r"<https?:\/\/([^\|]+)\|*.*\>"
            match = re.search(re_pattern, msg_txt, flags=re.UNICODE)
            if match:
                title = match.group(1)

                for domain in env.URL_BLACKLIST:
                    if title.find(domain) != -1: return

                response = self.clients.web.users.info(event['user'])
                username = response.body['user']['name']

                if event['channel'][0] == 'G':
                    response = self.clients.web.groups.info(event['channel'])
                    channel = response.body['group']['name']
                elif event['channel'][0] == 'D':
                    channel = "DM"
                elif event['channel'][0] == 'C':
                    response = self.clients.web.channels.info(event['channel'])
                    channel = response.body['channel']['name']
                source = "{}@{}".format(username, channel)

                msg = msg_txt.replace('<','').replace('>','')

                payload = {
                    "value1" : title,
                    "value2" : source,
                    "value3" : msg
                    }
                logger.debug(json.dumps(payload))
                url = "https://maker.ifttt.com/trigger/{}/with/key/{}".format(env.IFTTT_EVENT, env.IFTTT_TOKEN)
                requests.post(url, json=payload)

                # client = Algorithmia.client(env.ALGO_TOKEN)

                # algo_text = client.algo('util/Html2Text/0.1.4')
                # algo_summary = client.algo('nlp/Summarizer/0.1.3')

                # link_text = algo_text.pipe(title).result
                # summary = algo_summary.pipe(link_text).result

                # channel_id = event['channel']
                # msg = "Summary: {}".format(summary)
                # self.msg_writer.send_message(channel_id, msg)

            # if self.clients.is_bot_mention(msg_txt):
            #     # e.g. user typed: "@pybot tell me a joke!"
            #     if 'help' in msg_txt:
            #         self.msg_writer.write_help_message(event['channel'])
            #     elif re.search('hi|hey|hello|howdy', msg_txt):
            #         self.msg_writer.write_greeting(event['channel'], event['user'])
            #     elif 'joke' in msg_txt:
            #         self.msg_writer.write_joke(event['channel'])
            #     elif 'attachment' in msg_txt:
            #         self.msg_writer.demo_attachment(event['channel'])
            #     elif 'echo' in msg_txt:
            #         self.msg_writer.send_message(event['channel'], msg_txt)
            #     else:
            #         self.msg_writer.write_prompt(event['channel'])
