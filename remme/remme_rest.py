import requests


class RemmeRest:

    network_config = None

    def __init__(self, network_config):
        self.network_config = network_config
        protocol = 'https' if self.network_config['ssl_mode'] else 'http'
        self.node_url = protocol + "://" + self.network_config['node_address'] + ":" + self.network_config['node_port']

    def send_request(self, **kwargs):
        url = self.node_url + kwargs['url']
        data = kwargs['data'] if 'data' in kwargs else None
        r = kwargs['request'](url, json=data)
        if r.status_code == 200:
            return {'status': "OK", 'data': r.json()}
        return {'status': "ERROR"}

    def get(self, **kwargs):
        kwargs['request'] = requests.get
        return self.send_request(**kwargs)

    def post(self, **kwargs):
        kwargs['request'] = requests.post
        return self.send_request(**kwargs)

    def put(self, **kwargs):
        kwargs['request'] = requests.put
        return self.send_request(**kwargs)

    def delete(self, **kwargs):
        kwargs['request'] = requests.delete
        return self.send_request(**kwargs)
