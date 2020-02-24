from errbot import BotPlugin, botcmd


class HelloWorld(BotPlugin):
    """Hello World Bot."""

    @botcmd
    def hello(self, msg, args):
        """Says hello world. :)"""
        return "Hello World :raised_hands:"

