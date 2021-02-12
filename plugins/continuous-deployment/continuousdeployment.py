import os
import subprocess

from errbot import BotPlugin, botcmd
from errbot.utils import global_restart


class ContinuousDeployment(BotPlugin):
    """Bot which when asked will perform release to production."""

    RELEASE_SCRIPT = os.environ.get("RELEASE_SCRIPT", default=None)
    BOT_UPDATE_SCRIPT = os.environ.get("BOT_UPDATE_SCRIPT", default=None)
    ATTENDANCE_PROCESSOR_SCRIPT = os.environ.get("ATTENDANCE_PROCESSOR_SCRIPT", default=None)
    ENROLLMENT_PROCESSOR_SCRIPT = os.environ.get("ENROLLMENT_PROCESSOR_SCRIPT", default=None)
    HASH_FILE_PATH = os.environ.get("HASH_FILE_PATH", default=None)
    GITHUB_URL = os.environ.get("GITHUB_URL", default=None)

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
    def release_attendance_processor(self, msg, args):
        """Perform release of the attendance processor."""
        if not self.ATTENDANCE_PROCESSOR_SCRIPT:
            raise Exception("No attendance processor release script configured. :persevere:")

        try:
            yield "Releasing attendance processor... hang on tight :rocket:"
            subprocess.call([self.ATTENDANCE_PROCESSOR_SCRIPT])
            yield "{} attendance processor is now released! :sunglasses:".format(
                msg.frm.person
            )
        except OSError:
            raise Exception("Failed to run attendance processor release script... :disappointed:")

    @botcmd
    def release_enrollment_processor(self, msg, args):
        """Perform release of the enrollment processor."""
        if not self.ENROLLMENT_PROCESSOR_SCRIPT:
            raise Exception("No enrollment processor release script configured. :persevere:")

        try:
            yield "Releasing enrollment processor... hang on tight :rocket:"
            subprocess.call([self.ENROLLMENT_PROCESSOR_SCRIPT])
            yield "{} enrollment processor is now released! :sunglasses:".format(
                msg.frm.person
            )
        except OSError:
            raise Exception("Failed to run enrollment processor release script... :disappointed:")

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

    @botcmd
    def show_changes(self, msg, args):
        """Shows git changes between master and what's released"""
        if not self.HASH_FILE_PATH:
            raise Exception("No hash file path configured... :disappointed:")
        if not self.GITHUB_URL:
            raise Exception("No github url configured... :disappointed:")

        with open(self.HASH_FILE_PATH, 'r', encoding="utf-8") as hash_file:
            compare_hash = hash_file.readline().strip('\n')

            compare_url = "{}compare/{}...master".format(self.GITHUB_URL, compare_hash)
            return compare_url
