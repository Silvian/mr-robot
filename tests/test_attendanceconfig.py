from unittest.mock import MagicMock

pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = 'plugins'


def test_get_max_attendees(testbot):
    get_value = '200'
    helper_mock = MagicMock(return_value=get_value)
    mock_dict = {'retrieve_max_attendees': helper_mock}
    testbot.inject_mocks('AttendanceConfig', mock_dict)
    testbot.push_message('!get max attendees')
    expected = get_value
    result = testbot.pop_message()
    assert result == expected


def test_set_max_attendees(testbot):
    set_value = '50'
    helper_mock = MagicMock(return_value=set_value)
    mock_dict = {'update_max_attendees': helper_mock}
    testbot.inject_mocks('AttendanceConfig', mock_dict)
    testbot.push_message(f'!set max attendees {set_value}')
    expected = f'Max attendees is now set to {set_value}.'
    result = testbot.pop_message()
    assert result == expected


def test_set_max_attendees_no_args(testbot):
    testbot.push_message('!set max attendees')
    assert (
        "Please provide a number of attendees allowed. :persevere:"
        in
        testbot.pop_message()
    )
