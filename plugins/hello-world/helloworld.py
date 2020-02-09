from errbot import BotPlugin, botcmd


class HelloWorld(BotPlugin):
    """Hello World Bot."""

    @botcmd
    def hello(self, msg, args):
        return "Hello World :raised_hands:"

