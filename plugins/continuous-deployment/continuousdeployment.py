import os
import subprocess

from errbot import BotPlugin, botcmd
from errbot.utils import global_restart


class ContinuousDeployment(BotPlugin):
    """Bot which when asked will perform release to production."""

    RELEASE_SCRIPT = os.environ.get("RELEASE_SCRIPT", default=None)
    BOT_UPDATE_SCRIPT = os.environ.get("BOT_UPDATE_SCRIPT", default=None)

    @botcmd
    def release_production(self, msg, args):
        """Perform release to production environment."""
        if not self.RELEASE_SCRIPT:
            raise Exception("No release script configured. :persevere:")

        try:
            yield "Releasing to production... hang on tight :wink:"
            subprocess.call([self.RELEASE_SCRIPT])
            yield "{} release to production is now complete! :sunglasses:".format(
                msg.frm.person
            )
        except OSError:
            raise Exception("Failed to run release script... :disappointed:")

    @botcmd
    def self_update(self, msg, args):
        """Perform a release update of the bot."""
        if not self.BOT_UPDATE_SCRIPT:
            raise Exception("No update script configured. :persevere:")

        try:
            yield "Improving myself..."
            subprocess.call([self.BOT_UPDATE_SCRIPT])
            yield "A newer, a better me... :smile:"
            self.send(msg.frm, "Deactivating all the plugins...")
            self._bot.plugin_manager.deactivate_all_plugins()
            self.send(msg.frm, "I'm restarting now...")
            self._bot.shutdown()
            global_restart()
        except OSError:
            raise Exception("Failed to run update script... :disappointed:")
