# -*- coding: utf-8 -*-
# @Time    : 2020-11-19 11:25
# @Author  : xzr
# @File    : zeppelin_pyclient
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :

import requests


class ZeppelinClient(object):
    """
    Zeppelin python Client
    http://zeppelin.apache.org/docs/0.9.0-preview2/usage/rest_api/notebook.html
    """
    API_HOST = ''
    API_PATH = ''

    def __init__(self, api_address: str, username, password, timeout=5):
        self.api_address = api_address.rstrip('/')
        self.timeout = timeout
        self.s = None
        self.username = username
        self.passowrd = password

    def set_timeout(self, timeout):
        self.timeout = timeout or self.timeout

    def generate_url(self, path: str):
        return self.api_address + path

    def create_note(self, *names):
        note_name = '/'.join(names)
        path = '/api/notebook'
        data = {"name": note_name, 'defaultInterpreterGroup': 'flink'}
        result = self.req('POST', path, json=data)
        return result

    def create_note_and_paragraphs(self, note_name, paragraphs_list):
        path = '/api/notebook'
        data = {"name": note_name, "defaultInterpreterGroup": "flink", "paragraphs": paragraphs_list}
        result = self.req('POST', path, json=data)
        return result

    def get_note_info(self, note_id):
        path = '/api/notebook/' + note_id
        result = self.req('GET', path)
        return result

    def get_notes(self):
        """
        List of the notes
        :return:
        """

        path = '/api/notebook'
        rsp = self.req('GET', path)
        return rsp.json()

    def get_all_paragraphs(self, note_id: str):
        path = '/api/notebook/job/' + note_id
        result = self.req('GET', path)
        return result

    def run_all_paragraphs(self, note_id):
        path = '/api/notebook/job/' + note_id
        result = self.req('POST', path)
        return result

    def stop_all_paragraphs(self, note_id):
        path = '/api/notebook/job/' + note_id
        result = self.req('DELETE', path)
        return result

    def delete_note(self, note_id: str):
        path = '/api/notebook/' + note_id
        result = self.req('DELETE', path)
        return result

    def rename_note(self, note_id, *new_names):
        new_note_name = '/'.join(new_names)
        path = '/api/notebook/' + note_id + '/rename'
        data = {"name": new_note_name}
        result = self.req('PUT', path, json=data)
        return result

    def create_paragraph(self, note_id, title, text, index=0):
        path = '/api/notebook/' + note_id + '/paragraph'
        data = {"title": title,
                "text" : text,
                }
        if index:
            data['index'] = index
        result = self.req('POST', path, json=data)
        paragraph_id = result['body']
        return result

    def get_paragraph_info(self, note_id, paragraph_id):
        path = '/api/notebook/' + note_id + '/paragraph/' + paragraph_id

        result = self.req('GET', path)
        return result

    def get_paragraph_status(self, note_id, paragraph_id):
        path = '/api/notebook/job/' + note_id + '/' + paragraph_id
        result = self.req('GET', path)
        return result

    def update_paragraph(self, note_id, paragraph_id, title, text):
        path = '/api/notebook/' + note_id + '/paragraph/' + paragraph_id
        data = {"title": title,
                "text" : text,
                }
        result = self.req('PUT', path, json=data)
        return result

    def delete_paragraph(self, note_id, paragraph_id):
        path = '/api/notebook/' + note_id + '/paragraph/' + paragraph_id

        result = self.req('DELETE', path)
        return result

    def run_paragraph_async(self, name, note_id, paragraph_id, params={}):
        path = '/api/notebook/job/' + note_id + '/' + paragraph_id
        data = dict(name=name)
        if params:
            data['params'] = params
        result = self.req('POST', path, json=data)
        return result

    def run_paragraph_sync(self, name, note_id, paragraph_id, params={}, timeout=None):
        path = '/api/notebook/run/' + note_id + '/' + paragraph_id
        data = dict(name=name)
        self.set_timeout(timeout)
        if params:
            data['params'] = params
        result = self.req('POST', path, json=data)

        return result

    def stop_paragraph(self, note_id, paragraph_id):
        path = '/api/notebook/job/' + note_id + '/' + paragraph_id
        result = self.req('DELETE', path)
        return result

    def move_paragraph_index(self, note_id, paragraph_id, new_index):
        path = '/api/notebook/' + note_id + '/paragraph/' + paragraph_id + '/move/' + str(new_index)
        result = self.req('POST', path)

        return result

    def restart_interpreter(self, note_id, interpreter):

        path = '/api/interpreter/setting/restart/%s' % interpreter
        data = {"noteId": note_id}
        result = self.req('PUT', path, json=data)
        return result

    def req(self, method, path, **kwargs):
        self.s = self.s or requests.Session()
        url = self.generate_url(path)
        rsp = self.s.request(method, url, timeout=self.timeout, **kwargs)

        result = rsp.json()
        if rsp.status_code != 200:
            raise Exception('Unable to call %s [%s] rest api, status: %s, message: %s' % (url,method,rsp.status_code, rsp.content))

        return result


if __name__ == '__main__':
    zc = ZeppelinClient('http://master:18080/')
    import pprint

    pp = pprint.pprint
    pp(zc.get_notes())
    pp(zc.get_all_paragraphs('2F2YS7PCE'))
