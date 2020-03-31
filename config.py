import os
import logging

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = 'Text'  # Errbot will start in Text mode.
ENVIRONMENTS = ("staging", "production")
BOT_DATA_DIR = r'data'
BOT_EXTRA_PLUGIN_DIR = r'plugins'

BOT_LOG_FILE = r'errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

BOT_ALT_PREFIXES = ('@mr_robot',)
BOT_ADMINS = os.environ.get("BOT_ADMINS", default="@admin").split(",")

if os.environ.get("ENVIRONMENT", default=None) in ENVIRONMENTS:
    BACKEND = 'Slack'  # Errbot will start in Slack mode.
    ACCESS_CONTROLS_DEFAULT = {'allowusers': BOT_ADMINS}  # Only admins are allowed to perform any actions.

    BOT_LOG_FILE = os.environ.get("LOG_FILE", default=r'errbot.log')
    BOT_LOG_LEVEL = logging.INFO

    # Security configurations:
    HIDE_RESTRICTED_COMMANDS = True
    HIDE_RESTRICTED_ACCESS = True

# Slack API token
BOT_IDENTITY = {
    'token': os.environ.get("BOT_IDENTITY_KEY", default=None)
}
