import pytest

from unittest import mock
from unittest.mock import MagicMock

pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = 'plugins'


def test_weather(testbot):
    expected_result = 'The weather in London, United Kingdom is Clear, with a temperature 10 deg'
    helper_mock = MagicMock(return_value=expected_result)
    mock_dict = {'get_weather_api': helper_mock}
    testbot.inject_mocks('Weather', mock_dict)
    testbot.push_message('!get weather London')
    result = testbot.pop_message()
    assert result == expected_result


def test_weather_no_args(testbot):
    expected_result = 'Please specify a city name.'
    testbot.push_message('!get weather')
    assert expected_result in testbot.pop_message()


def test_get_weather_api_no_key(testbot):
    weather = testbot._bot.plugin_manager.get_plugin_obj_by_name('Weather')
    expected = "No weather api key configured. :persevere:"
    with pytest.raises(Exception):
        result = weather.get_weather_api("London")
        assert result == expected


@mock.patch("requests.get")
def test_get_weather_api_exception(mock_request, testbot):
    weather = testbot._bot.plugin_manager.get_plugin_obj_by_name('Weather')
    weather.WEATHER_API_KEY = "secret_key"
    expected = "Weather exception: server error"
    mock_request.return_value.status_code = 400
    mock_request.return_value.text = "server error"
    with pytest.raises(Exception):
        result = weather.get_weather_api("London")
        assert result == expected


@mock.patch("requests.get")
def test_get_weather_api_response_exception(mock_request, testbot):
    weather = testbot._bot.plugin_manager.get_plugin_obj_by_name('Weather')
    weather.WEATHER_API_KEY = "secret_key"
    expected = "Weather exception: data error"
    mock_request.return_value.status_code = 200
    response_data = {
        "error": {
            "info": "data error",
        }
    }
    mock_request.return_value.json.return_value = response_data
    with pytest.raises(Exception):
        result = weather.get_weather_api("London")
        assert result == expected


@mock.patch("requests.get")
def test_get_weather_api_response_success(mock_request, testbot):
    weather = testbot._bot.plugin_manager.get_plugin_obj_by_name('Weather')
    weather.WEATHER_API_KEY = "secret_key"
    expected = 'The weather in London, United Kingdom is Clear, with a temperature 10 deg'
    mock_request.return_value.status_code = 200
    response_data = {
        "success": "true",
        "location": {
            "name": "London",
            "country": "United Kingdom",
        },
        "current": {
            "temperature": 10,
            "weather_descriptions": ["Clear"],
        }
    }
    mock_request.return_value.json.return_value = response_data
    result = weather.get_weather_api("London")
    assert result == expected
