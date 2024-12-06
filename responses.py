import os
import logging
import json


class JsonEditor:
    def __init__(self, json_file):
        self.json_file = json_file
        if not os.path.exists(self.json_file):
            os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
            with open(self.json_file, 'w') as new_file:
                new_file.write('{}')
                new_file.close()
                logging.info(f'Created new JSON file "{self.json_file}".')
        with open(self.json_file) as file:
            self.data = json.load(file)
            logging.info(f'Loaded JSON data from "{self.json_file}".')
            file.close()


class Responses(JsonEditor):
    def __init__(self, json_file):
        self.path = os.path.join(os.getcwd(), 'responses', json_file)
        JsonEditor.__init__(self, self.path)

    def return_response(self):
        logging.info(f'Returning data from "{self.path}"')
        # logging.debug(f'{self.data}.')
        return self.data
