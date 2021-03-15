from unittest.mock import MagicMock

pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = 'plugins'


def test_kenye_west_quote(testbot):
    kenye_quote = 'I seem to have lost myself'
    helper_mock = MagicMock(return_value=kenye_quote)
    mock_dict = {'kanye_rest': helper_mock}
    testbot.inject_mocks('Fun', mock_dict)
    testbot.push_message('!kanye west quote')
    expected = f'Kanye West says: {kenye_quote}'
    result = testbot.pop_message()
    assert result == expected


def test_cat_facts(testbot):
    cat_fact = 'Cats are better than dogs!'
    helper_mock = MagicMock(return_value=cat_fact)
    mock_dict = {'get_cat_facts': helper_mock}
    testbot.inject_mocks('Fun', mock_dict)
    testbot.push_message(f'!cat facts')
    expected = cat_fact
    result = testbot.pop_message()
    assert result == expected


def test_meme(testbot):
    expected = "This is a meme..."
    helper_mock = MagicMock(return_value=expected)
    mock_dict = {'get_memes': helper_mock}
    testbot.inject_mocks('Fun', mock_dict)
    testbot.push_message(f'!meme')
    result = testbot.pop_message()
    assert result == expected
