"""Config storage and query for a application.
"""
import copy
import json
import os
import getpass
import socket
import re
import tempfile


class Borg(object):
    __shared_dict = {}
    def __init__(self):
        self.__dict__ = self.__shared_dict


class EnvVariableExpander(Borg):

    def __init__(self):
        Borg.__init__(self)

        self._populate_default_values()

    def __getitem__(self, key):
        # convert the key to lower case
        key = "_%s" % key.lower()
        if key in self.__dict__.keys():
            return getattr(self, key)
        raise KeyError

    def _populate_default_values(self):
        self._host = socket.gethostname()
        self._user = getpass.getuser()
        self._home = os.path.expanduser('~')
        self._temp = tempfile.gettempdir()

    def convert_str(self, string):
        _regex = re.compile("\$\w+")
        new_string = string
        error_conversion = False
        for var in _regex.findall(string):
            try:
                new_string = re.sub(
                    "\%s" % var,
                    self[var[1:]],
                    new_string
                )
            except KeyError:
                error_conversion = True

        return (not error_conversion, new_string)


class Config(object):
    """Config class to manage config json files.
    """

    def __init__(self, file_path):
        """Constructor

        Keyword Args:
            file_path (str, optional): Defaults to None. The config file file_path.
        """
        self.file_path = None
        self.set_config_path(file_path)

    def __getitem__(self, key):
        """Overrides the attribute getter to get the config data
        as attributes of the Config instance.
        eg. config["path"]

        Args:
            key (str): The config data that we need.

        Returns:
            python data: The value stored in the config.
        """
        return getattr(self, key)

    def __str__(self):
        """String representation for display
        """
        return 'Config file_path: {}'.format(self.file_path)

    def load_config(self):
        """Load the json and set the attributes.
        eg. config.path
        """
        data = self.get_config_data()
        for key, value in data.iteritems():
            self.__dict__[key] = value

    def get_config_data(self):
        """Load the json data.

        Returns:
            dict : The converted json data.
        """
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return data or {}

    def set_config_path(self, file_path):
        """Set the config pathself.

        Args:
            file_path (str): The config path.
        """
        if os.path.exists(file_path):
            self.file_path = file_path

    def write_config(self, dict_data, append=True):
        """Save out the dictionary data into a config file.

        Args:
            dict_data (dict): The Config data in keys and values.
            append (bool, optional): Defaults to True, if set open the
            existing file and update the data.
        """
        data = self.get_config_data() if append else {}
        data.update(dict_data)

        with open(self.file_path, 'w') as f:
            json.dump(data, f)
