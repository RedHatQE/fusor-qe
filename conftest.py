"""
This file specifies fixtures that are located under the plugins directory.
Any files added to the plugin directory will need to be listed below for
py.test to load it.
"""

pytest_plugins = "plugin.selenium",\
    "plugin.navigation"
