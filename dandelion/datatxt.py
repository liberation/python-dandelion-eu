""" classes for querying the dataTXT family
"""
import json

from dandelion.base import BaseDandelionRequest
from dandelion.base import MissingParameterException


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
        if not self.model:
            raise MissingParameterException("model")
        return self.do_request(
            dict(params, text=text, model=self.model), ('cl', 'v1')
        )

    def _get_uri_tokens(self):
        return 'datatxt',


class ClassifierCrud(BaseDandelionRequest):
    """ Classifier crud api integration.
    """

    def read(self, model_id, **params):
        return self.do_request(
            dict(params, id=model_id), ('cl', 'models', 'v1'), method='get'
        )

    def create(self, data, **params):
        return self.do_request(
            dict(params, data=json.dumps(data)), ('cl', 'models', 'v1')
        )

    def update(self, data, model_id, **params):
        return self.do_request(
            dict(params, id=model_id, data=json.dumps(data)),
            ('cl', 'models', 'v1'), method='put'
        )

    def delete(self, model_id, **params):
        return self.do_request(
            dict(params, id=model_id), ('cl', 'models', 'v1'), method='delete'
        )

    def list(self):
        return self.do_request(
            {}, ('cl', 'models', 'v1'), method='get'
        )

    def _get_uri_tokens(self):
        return 'datatxt',
