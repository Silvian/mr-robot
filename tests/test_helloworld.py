pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = 'plugins'


def test_hello_command(testbot):
    testbot.push_message('!hello')
    assert "Hello World :raised_hands:" in testbot.pop_message()
