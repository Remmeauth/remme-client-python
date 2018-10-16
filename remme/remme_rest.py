import requests


class RemmeRest:

    node_address = None
    node_port = None
    ssl_mode = None
    node_url = None

    def __init__(self, network_config):
        self.node_address = network_config['node_address']
        self.node_port = network_config['node_port']
        self.ssl_mode = network_config['ssl_mode']
        protocol = 'https' if self.ssl_mode else 'http'
        self.node_url = protocol + "://" + self.node_address + ":" + self.node_port

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

    def get_node_socket(self):
        return self.node_address + ':' + self.node_port

    def get_ssl_mode(self):
        return self.ssl_mode
