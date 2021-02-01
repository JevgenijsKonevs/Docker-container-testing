import subprocess
import os

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


def run_cmd(ip, params, check_str, pos="passed", neg="failed"):
    params.append(ip)
    process = subprocess.Popen(
        params,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, errors = process.communicate()
    process.wait()

    data = output.decode('utf-8') + errors.decode('utf-8')

    if check_str in data:
        return pos, data
    return neg, data


class REST_server_http(Resource):
    def get(self):
        params = ['curl', '-IS']
        ip = os.environ['container_b_ip']

        test_result, debug = run_cmd(
            f'{ip}:80', params, 'Content-Type: text/html')
        return {"http": test_result, "debug": debug}


class REST_server_ssh(Resource):
    def get(self):
        params = ['ssh', '-tt',
                  '-o', 'PubkeyAuthentication=no',
                  '-o', 'PasswordAuthentication=no',
                  '-o', 'KbdInteractiveAuthentication=no',
                  '-o', 'ChallengeResponseAuthentication=no',
                  '-o', 'StrictHostKeyChecking=no'
                  ]
        ip = os.environ['container_b_ip']

        test_result, debug = run_cmd(f'{ip}', params, 'Permission denied')
        return {"ssh": test_result, "debug": debug}


class REST_server_ping(Resource):
    def get(self):
        params = ['ping', '-c', '1']
        ip = os.environ['container_b_ip']

        test_result, debug = run_cmd(
            f'{ip}', params, 'Unreachable', pos="failed", neg="passed")
        return {"ping": test_result, "debug": debug}


class REST_server_all(Resource):
    def get(self):
        http = REST_server_http().get()
        ssh = REST_server_ssh().get()
        ping = REST_server_ping().get()

        return {"data": {"http": http, "ssh": ssh, "ping": ping}}


api.add_resource(REST_server_http, "/http")
api.add_resource(REST_server_ssh, "/ssh")
api.add_resource(REST_server_ping, "/ping")
api.add_resource(REST_server_all, "/tests")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
