import time
import config
import utils
from flask import Flask, request, jsonify, Response
from datetime import datetime
from data_access.db_client import MysqlClient
from data_access.dao import BodyMetricsDAO
from exceptions import RequestNotFoundError, BadRequestError, InternalError

app = Flask(__name__)

mysql_client = MysqlClient(config.DB_HOST, config.DB_USERNAME,
                           config.DB_PW, config.DB_NAME)
body_metrics_dao = BodyMetricsDAO(mysql_client)


@app.route('/body_metrics/')
def hello_world():  # put application's code here
    return 'Welcome to ShapeMentor Body Metrics Microservice!'


@app.route('/body_metrics/health', methods=['GET'])
def check_health():
    return {'msg': 'server is healthy!', 'datetime': datetime.now()}


@app.route('body_metrics/users/<user_id>/upload_data', methods=['POST'])
def upload_user_body_metrics_data(user_id: str):
    request_data = request.json
    upload_timestamp = datetime.utcnow().isoformat()
    request_data['data']['user_id'] = user_id
    request_data['data']['timestamp'] = upload_timestamp

    request_data = utils.transform_body_metrics_upload_data(request_data)

    if request_data is None:
        raise BadRequestError

    try:
        if not body_metrics_dao.write_user_body_metrics_data(request_data):
            raise InternalError

        return success_rsp({'user_id': user_id, 'upload_time': upload_timestamp})

    except Exception as e:
        if isinstance(e, BadRequestError):
            raise BadRequestError
        print(f'unexpected exceptions: {e}')
        raise InternalError


@app.route('body_metrics/users/<user_id>/retrieve_data', methods=['GET'])
def get_user_body_metrics_data(user_id: str):
    try:
        retrieved_user_data = body_metrics_dao.get_user_body_metrics_data(user_id)

        if retrieved_user_data is None:
            raise RequestNotFoundError

        return success_rsp(retrieved_user_data)

    except Exception as e:
        if isinstance(e, RequestNotFoundError):
            raise RequestNotFoundError
        print(f'unexpected exceptions: {e}')
        raise InternalError


@app.errorhandler(RequestNotFoundError)
@app.errorhandler(BadRequestError)
@app.errorhandler(InternalError)
def handle_error(error):
    response = jsonify({'error': error.message, 'status_code': error.status_code})
    response.status_code = error.status_code
    return response


def success_rsp(data) -> Response:
    rsp = {'status_code': 200, 'data': data}
    return jsonify(rsp)


if __name__ == '__main__':
    app.run()
