""" classes for querying the dataTXT family
"""
import json

from dandelion.base import BaseDandelionRequest


class DataTXT(BaseDandelionRequest):
    """ class for accessing the dataTXT family
    """
    def nex(self, text, **params):
        if 'min_confidence' not in params:
            params['min_confidence'] = 0.6
        return self.do_request(
            dict(params, text=text), ('nex', 'v1')
        )

    def sim(self, text1, text2, **params):
        return self.do_request(
            dict(params, text1=text1, text2=text2), ('sim', 'v1')
        )

    def li(self, text, **params):
        return self.do_request(
            dict(params, text=text), ('li', 'v1')
        )

    def cl(self, text, **params):
        return self.do_request(
            dict(params, text=text), ('cl', 'v1')
        )

    def _get_uri_tokens(self):
        return 'datatxt',


class ClassifierCrud(BaseDandelionRequest):
    """ Classifier crud api integration.
    """

    def read(self, model_id, **params):
        return self.do_request(
            dict(params, id=model_id), ('li', 'models', 'v1'), method='get'
        )

    def create(self, data, **params):
        return self.do_request(
            dict(params, data=json.dumps(data)), ('li', 'models', 'v1')
        )

    def update(self, data, model_id, **params):
        return self.do_request(
            dict(params, id=model_id, data=json.dumps(data)),
            ('li', 'models', 'v1'), method='put'
        )

    def delete(self, model_id, **params):
        return self.do_request(
            dict(params, id=model_id), ('li', 'models', 'v1'), method='delete'
        )

    def list(self):
        return self.do_request(
            {}, ('li', 'models', 'v1'), method='get'
        )

    def _get_uri_tokens(self):
        return 'datatxt',
