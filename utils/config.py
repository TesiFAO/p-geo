import json


class Config:

    def __init__(self, filename):

        """
        Initialize the class with the filename of a JSON stored in the config directory.
        @param filename: Name of the JSON file stored in the config lib to be read
        """

        self.filename = filename
        # TODO fix the problem about the path
        json_data = open('../config/' + self.filename + '.json').read()
        # json_data = open('../../config/' + self.filename + '.json').read()
        # json_data = open(self.filename + '.json').read()
        self.config = json.loads(json_data)

    def get(self, property):
        """
        Read a property of the JSON file stored in the config directory and set in the constructor.
        @param property: Name of the JSON key to access the property
        @return: Value corresponding to the given key
        """
        return self.config[property]