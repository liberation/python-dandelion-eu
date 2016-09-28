""" tests can be run from the root dir with:
clean-pyc && \
APP_ID= APP_KEY= coverage run --source=. --branch `which nosetests` tests/* &&\
coverage html
"""
import os
from unittest import TestCase

from mock import patch

from dandelion import Datagem, DandelionException, DataTXT, default_config
from dandelion.base import BaseDandelionRequest
from dandelion.utils import AttributeDict


class TestDefaultConfiguration(TestCase):
    def tearDown(self):
        # cleanup default config
        for key in ['token']:
            if key in default_config:
                del default_config[key]

    def test_can_set_token(self):
        default_config['token'] = os.environ['TOKEN']
        dg = Datagem('administrative-regions')
        self.assertEquals(
            dg.token,
            os.environ['TOKEN']
        )

    def test_can_authenticate(self):
        with self.assertRaises(DandelionException) as context:
            Datagem('administrative-regions')
        self.assertEqual(
            context.exception.message, 'Param "token" is required'
        )

        with self.assertRaises(DandelionException) as context:
            DataTXT()
        self.assertEqual(
            context.exception.message, 'Param "token" is required'
        )

        default_config['token'] = os.environ['TOKEN']

        Datagem('administrative-regions')
        DataTXT()

    def test_cannot_set_other_params(self):
        with self.assertRaises(DandelionException) as context:
            default_config['foo'] = 42

        self.assertEqual(
            context.exception.message, "invalid config param: foo"
        )


class TestAttributeDict(TestCase):
    def test_simple(self):
        obj = AttributeDict()

        obj.name = 'foo'
        self.assertEqual(obj.name, 'foo')

        del obj.name
        with self.assertRaises(KeyError):
            print(obj.name)


class TestBaseClass(TestCase):

    @staticmethod
    def _make_class(require_auth=True, implement_abstract=False):
        class TestClass(BaseDandelionRequest):
            REQUIRE_AUTH = require_auth

            def _get_uri_tokens(self):
                if implement_abstract:
                    return ['']
                return super(TestClass, self)._get_uri_tokens()

        return TestClass

    def test_abstract_methods(self):
        with self.assertRaises(NotImplementedError):
            self._make_class(require_auth=False)()

    def test_authentication_required(self):
        with self.assertRaises(DandelionException) as context:
            self._make_class(require_auth=True, implement_abstract=True)()

        self.assertEqual(
            context.exception.message, 'Param "token" is required'
        )

        obj = self._make_class(require_auth=True, implement_abstract=True)(
            token='aa'
        )
        with patch.object(obj, '_do_raw_request') as _do_raw_request:
            _do_raw_request.return_value.ok = True
            _do_raw_request.return_value.content = '{}'
            obj.do_request(params=dict(foo='bar'))

            _do_raw_request.assert_called_once_with(
                'https://api.dandelion.eu',
                {'foo': 'bar', 'token': 'aa'},
                'post'
            )

    def test_authentication_not_required(self):
        obj = self._make_class(require_auth=False, implement_abstract=True)()
        with patch.object(obj, '_do_raw_request') as _do_raw_request:
            _do_raw_request.return_value.ok = True
            _do_raw_request.return_value.content = '{}'
            obj.do_request(params=dict(foo='bar'))

            _do_raw_request.assert_called_once_with(
                'https://api.dandelion.eu', dict(foo='bar'), 'post'
            )
