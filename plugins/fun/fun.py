import re
import requests

from errbot import BotPlugin, botcmd, re_botcmd


class Fun(BotPlugin):
    """A little bit of fun and games."""

    KANYE_REST_API = "https://api.kanye.rest"
    CAT_FACT_API = "https://catfact.ninja/fact"
    MEMES_API = "https://meme-api.herokuapp.com/gimme"

    @re_botcmd(pattern=r"(^| )kanye?( |$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_talk_of_kanye_west(self, msg, match):
        """Listens for any mention of Kanye West."""
        return "Kanye West says: {}".format(self.kanye_rest())

    @re_botcmd(pattern=r"(^| )cat[s]?( |$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_talk_of_cats(self, msg, match):
        """Listenst for any mention of cats."""
        return self.get_cat_facts()

    @re_botcmd(pattern=r"(^| )meme[s]?( |$)", prefixed=False, flags=re.IGNORECASE)
    def listen_memes(self, msg, match):
        """Listens for any mention of memes."""
        return self.get_memes()

    @botcmd
    def kanye_west_quote(self, msg, args):
        """Provides a Kanye West Quote."""
        return "Kanye West says: {}".format(self.kanye_rest())

    @botcmd
    def cat_facts(self, msg, args):
        """Provides a cat fact."""
        return self.get_cat_facts()

    @botcmd
    def meme(self, msg, args):
        """Provides a meme."""
        return self.get_memes()
    
    def kanye_rest(self):
        response = requests.get(self.KANYE_REST_API).json()
        quote = response["quote"]
        return quote

    def get_cat_facts(self):
        response = requests.get(self.CAT_FACT_API).json()
        fact = response["fact"]
        return fact

    def get_memes(self):
        response = requests.get(self.MEMES_API).json()
        image = response["url"]
        return image
