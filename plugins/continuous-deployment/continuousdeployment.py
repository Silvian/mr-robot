import os
import subprocess

from errbot import BotPlugin, botcmd


class ContinuousDeployment(BotPlugin):
    """Bot which when asked will perform release to production."""

    RELEASE_SCRIPT = os.environ.get("RELEASE_SCRIPT", default=None)

    @botcmd
    def release_production(self, msg, args):
        if not self.RELEASE_SCRIPT:
            return "No release script configured. :persevere:"

        try:
            yield "Releasing to production... hang on tight :wink:"
            subprocess.call([self.RELEASE_SCRIPT])
            yield "{} Release to production is now complete! :sunglasses:".format(
                msg.frm.person
            )
        except OSError:
            return "Failed to run release script... :disappointed:"
