import re
import requests

from errbot import BotPlugin, botcmd, re_botcmd


class Fun(BotPlugin):
    """A little bit of fun and games."""

    KANYE_REST_API = "https://api.kanye.rest"
    CAT_FACT_API = "https://catfact.ninja/fact"

    @re_botcmd(pattern=r"(^| )kanye?( |$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_talk_of_kanye_west(self, msg, match):
        return "Kanye West says: {}".format(self.kanye_rest())

    @re_botcmd(pattern=r"(^| )cats?( |$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_talk_of_cats(self, msg, match):
        return self.get_cat_facts()

    @botcmd
    def kanye_west_quote(self, msg, args):
        return "Kanye West says: {}".format(self.kanye_rest())

    @botcmd
    def cat_facts(self, msg, args):
        return self.get_cat_facts()

    def kanye_rest(self):
        response = requests.get(self.KANYE_REST_API).json()
        quote = response["quote"]
        return quote

    def get_cat_facts(self):
        response = requests.get(self.CAT_FACT_API).json()
        fact = response["fact"]
        return fact
