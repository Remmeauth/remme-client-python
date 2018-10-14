import requests


class RemmeRest:

    network_config = None

    def __init__(self, network_config):
        self.network_config = network_config
        protocol = 'https' if self.network_config['ssl_mode'] else 'http'
        self.node_url = protocol + "://" + self.network_config['node_address'] + ":" + self.network_config['node_port']

    def get(self, *args, **kwargs):
        url = self.node_url + kwargs['url']
        r = requests.get(url)
        if r.status_code == 200:
            return {'status': "OK", 'data': r.json()}
        return {'status': "ERROR"}

    def post(self, *args, **kwargs):
        url = self.node_url + kwargs['url']
        data = kwargs['data']
        r = requests.post(url, json=data)
        if r.status_code == 200:
            return {'status': "OK", 'data': r.json()}
        return {'status': "ERROR"}

    def put(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
