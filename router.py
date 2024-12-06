import os
import logging
from logging import config
from flask import Flask, request, jsonify
from responses import Responses


logging.config.fileConfig(os.path.join(os.getcwd(), 'config', 'logconf.ini'))
logging = logging.getLogger('mock')


class Router:
    def __init__(self, name):
        self.app = Flask(name)

        @self.app.route('/api/v2/liveness', methods=['POST'])
        def __liveness_detection():
            transaction = request.args.get("transactionId")
            if not transaction:
                return jsonify({'error': 'no transaction id provided'}), 400
            logging.info(f'Working with transaction id: {transaction}')
            return jsonify(Responses('liveness_detection.json').return_response())

        @self.app.route('/api/detect', methods=['POST'])
        def __face_detection():
            data = request.json
            if 'processParam' not in data.keys():
                return jsonify(Responses('error_response.json').return_response()), 400
            return self.__verify_detect_type(data)

        @self.app.route('/api/match', methods=['POST'])
        def __face_matching():
            data = request.json
            if 'outputImageParams' not in data.keys():
                return jsonify(Responses('error_response.json').return_response()), 400
            return jsonify(Responses('face_matching.json').return_response())

    @staticmethod
    def __verify_detect_type(data):
        if 'attributes' in data['processParam'].keys():
            file = 'face_detection_all.json'
        elif 'scenario' in data['processParam'].keys():
            files = {'QualityICAO': 'face_quality_icao.json',
                     'QualityVisaUSA': 'face_quality_visa_usa.json',
                     'QualityVisaSchengen': 'face_quality_visa_schengen.json'}
            try:
                file = files[data['processParam']['scenario']]
            except KeyError:
                return jsonify(Responses('error_response.json').return_response()), 400
        else:
            file = 'face_detection_none.json'
        return jsonify(Responses(file).return_response())

    def run(self, host, port):
        self.app.run(host=host, port=port)


if __name__ == '__main__':
    server = Router(__name__)
    server.run(host="0.0.0.0", port="8080")