import os
import pytest

from unittest import mock
from unittest.mock import MagicMock

pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = 'plugins'


@mock.patch("subprocess.call")
def test_release_production(mock_subprocess_call, testbot):
    process_mock = MagicMock()
    attrs = {'communicate.return_value': ('output', 'error')}
    process_mock.configure_mock(**attrs)
    mock_subprocess_call.return_value = process_mock
    continuous_deployment = testbot._bot.plugin_manager.get_plugin_obj_by_name('ContinuousDeployment')
    continuous_deployment.RELEASE_SCRIPT = "release/script/path"
    testbot.push_message('!release production')
    assert "Releasing to production... hang on tight :wink:" in testbot.pop_message()
    assert mock_subprocess_call.called
    assert "release to production is now complete! :sunglasses:" in testbot.pop_message()


def test_release_production_no_script(testbot):
    testbot.push_message('!release production')
    expected = "No release script configured. :persevere:"
    with pytest.raises(Exception):
        result = testbot.pop_message()
        assert result == expected


def test_release_production_invalid_script_path(testbot):
    continuous_deployment = testbot._bot.plugin_manager.get_plugin_obj_by_name('ContinuousDeployment')
    continuous_deployment.RELEASE_SCRIPT = "release/script/path"
    testbot.push_message('!release production')
    assert "Releasing to production... hang on tight :wink:" in testbot.pop_message()
    with pytest.raises(Exception):
        expected_failure = "Failed to run release script... :disappointed:"
        result = testbot.pop_message()
        assert result == expected_failure


@mock.patch("subprocess.call")
def test_release_attendance_processor(mock_subprocess_call, testbot):
    process_mock = MagicMock()
    attrs = {'communicate.return_value': ('output', 'error')}
    process_mock.configure_mock(**attrs)
    mock_subprocess_call.return_value = process_mock
    continuous_deployment = testbot._bot.plugin_manager.get_plugin_obj_by_name('ContinuousDeployment')
    continuous_deployment.ATTENDANCE_PROCESSOR_SCRIPT = "release/script/path"
    testbot.push_message('!release attendance processor')
    assert "Releasing attendance processor... hang on tight :rocket:" in testbot.pop_message()
    assert mock_subprocess_call.called
    assert "attendance processor is now released! :sunglasses:" in testbot.pop_message()


def test_release_attendance_processor_no_script(testbot):
    testbot.push_message('!release attendance processor')
    expected = "No attendance processor release script configured. :persevere:"
    with pytest.raises(Exception):
        result = testbot.pop_message()
        assert result == expected


def test_release_attendance_processor_invalid_script_path(testbot):
    continuous_deployment = testbot._bot.plugin_manager.get_plugin_obj_by_name('ContinuousDeployment')
    continuous_deployment.ATTENDANCE_PROCESSOR_SCRIPT = "release/script/path"
    testbot.push_message('!release attendance processor')
    assert "Releasing attendance processor... hang on tight :rocket:" in testbot.pop_message()
    with pytest.raises(Exception):
        expected_failure = "Failed to run attendance processor release script... :disappointed:"
        result = testbot.pop_message()
        assert result == expected_failure


@mock.patch("subprocess.call")
def test_release_enrollment_processor(mock_subprocess_call, testbot):
    process_mock = MagicMock()
    attrs = {'communicate.return_value': ('output', 'error')}
    process_mock.configure_mock(**attrs)
    mock_subprocess_call.return_value = process_mock
    continuous_deployment = testbot._bot.plugin_manager.get_plugin_obj_by_name('ContinuousDeployment')
    continuous_deployment.ENROLLMENT_PROCESSOR_SCRIPT = "release/script/path"
    testbot.push_message('!release enrollment processor')
    assert "Releasing enrollment processor... hang on tight :rocket:" in testbot.pop_message()
    assert mock_subprocess_call.called
    assert "enrollment processor is now released! :sunglasses:" in testbot.pop_message()


def test_release_enrollment_processor_no_script(testbot):
    testbot.push_message('!release enrollment processor')
    expected = "No enrollment processor release script configured. :persevere:"
    with pytest.raises(Exception):
        result = testbot.pop_message()
        assert result == expected


def test_release_enrollment_processor_invalid_script_path(testbot):
    continuous_deployment = testbot._bot.plugin_manager.get_plugin_obj_by_name('ContinuousDeployment')
    continuous_deployment.ENROLLMENT_PROCESSOR_SCRIPT = "release/script/path"
    testbot.push_message('!release enrollment processor')
    assert "Releasing enrollment processor... hang on tight :rocket:" in testbot.pop_message()
    with pytest.raises(Exception):
        expected_failure = "Failed to run enrollment processor release script... :disappointed:"
        result = testbot.pop_message()
        assert result == expected_failure


@mock.patch("subprocess.call")
def test_self_update(mock_subprocess_call, testbot):
    process_mock = MagicMock()
    attrs = {'communicate.return_value': ('output', 'error')}
    process_mock.configure_mock(**attrs)
    mock_subprocess_call.return_value = process_mock
    continuous_deployment = testbot._bot.plugin_manager.get_plugin_obj_by_name('ContinuousDeployment')
    continuous_deployment.BOT_UPDATE_SCRIPT = "release/script/path"
    testbot.push_message('!self update')
    assert "Improving myself..." in testbot.pop_message()
    assert mock_subprocess_call.called
    assert "A newer, a better me... :smile:" in testbot.pop_message()


def test_self_update_no_script(testbot):
    testbot.push_message('!self update')
    expected = "No update script configured. :persevere:"
    with pytest.raises(Exception):
        result = testbot.pop_message()
        assert result == expected


def test_self_update_invalid_script_path(testbot):
    continuous_deployment = testbot._bot.plugin_manager.get_plugin_obj_by_name('ContinuousDeployment')
    continuous_deployment.BOT_UPDATE_SCRIPT = "release/script/path"
    testbot.push_message("!self update")
    assert "Improving myself..." in testbot.pop_message()
    with pytest.raises(Exception):
        expected_failure = "Failed to run update script... :disappointed:"
        result = testbot.pop_message()
        assert result == expected_failure


def test_show_changes(testbot):
    url_hash = "test-url-hash"
    continuous_deployment = testbot._bot.plugin_manager.get_plugin_obj_by_name('ContinuousDeployment')
    continuous_deployment.HASH_FILE_PATH = "./tests/github_hash.txt"
    continuous_deployment.GITHUB_URL = "https://github.com/test/url/"
    with open(continuous_deployment.HASH_FILE_PATH, "w") as f:
        f.write(url_hash + "\n")

    testbot.push_message('!show changes')
    expected = f"{continuous_deployment.GITHUB_URL}compare/{url_hash}...master"
    result = testbot.pop_message()
    assert result == expected

    if os.path.exists(continuous_deployment.HASH_FILE_PATH):
        os.remove(continuous_deployment.HASH_FILE_PATH)


def test_show_changes_missing_file_path(testbot):
    testbot.push_message('!show changes')
    expected = "No hash file path configured... :disappointed:"
    with pytest.raises(Exception):
        result = testbot.pop_message()
        assert result == expected


def test_show_changes_missing_github_url(testbot):
    continuous_deployment = testbot._bot.plugin_manager.get_plugin_obj_by_name('ContinuousDeployment')
    continuous_deployment.HASH_FILE_PATH = "hash/file/path"
    testbot.push_message('!show changes')
    expected = "No github url configured... :disappointed:"
    with pytest.raises(Exception):
        result = testbot.pop_message()
        assert result == expected
