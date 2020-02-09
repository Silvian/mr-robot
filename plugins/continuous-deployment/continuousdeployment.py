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
            subprocess.call([self.RELEASE_SCRIPT])
        except OSError:
            return "Failed to run release script... :disappointed:"

        return "Released to production! :sunglasses:"
