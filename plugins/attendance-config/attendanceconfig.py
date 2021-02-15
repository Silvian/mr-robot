import os
import requests

from errbot import BotPlugin, botcmd


class AttendanceConfig(BotPlugin):
    """AttendanceConfig for the attendance processor configuration values."""

    ATTENDANCE_CONFIG_API_URL = os.environ.get("ATTENDANCE_CONFIG_API_URL", None)
    ATTENDANCE_CONFIG_API_KEY = os.environ.get("ATTENDANCE_CONFIG_API_KEY", None)

    @botcmd
    def get_max_attendees(self, msg, args):
        """Retrieve the max number of attendees allowed."""
        if not self.ATTENDANCE_CONFIG_API_URL:
            raise Exception("No attendance config api url configured. :persevere:")

        if not self.ATTENDANCE_CONFIG_API_KEY:
            raise Exception("No attendance config api key configured. :persevere:")

        headers = {
            "Accept": "application/json",
            "x-api-key": f"{self.ATTENDANCE_CONFIG_API_KEY}",
        }
        url = self.ATTENDANCE_CONFIG_API_URL + "getAttendanceConfig"
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise Exception("Failed to retrieve result from the api. :persevere:")

        data = response.json()["body"]
        max_attendees = int(data["max"])
        return max_attendees

    @botcmd
    def set_max_attendees(self, msg, args):
        """Set the max number of attendees allowed."""
        if not args:
            raise Exception("Please provide a number of attendees allowed. :persevere:")

        if not self.ATTENDANCE_CONFIG_API_URL:
            raise Exception("No attendance config api url configured. :persevere:")

        if not self.ATTENDANCE_CONFIG_API_KEY:
            raise Exception("No attendance config api key configured. :persevere:")

        try:
            headers = {
                "Accept": "application/json",
                "x-api-key": f"{self.ATTENDANCE_CONFIG_API_KEY}",
            }
            data = {
                "max_value": int(args),
            }
            url = self.ATTENDANCE_CONFIG_API_URL + "updateAttendanceConfig"
            response = requests.post(url=url, json=data, headers=headers)
            if response.status_code != 200:
                raise Exception("Something went wrong! :persevere:")

            body = response.json()["body"]
            max_attendees = body["max"]
            return f"Max attendees is now set to {max_attendees}."

        except ValueError:
            raise Exception("Please provide a number... :cry:")
