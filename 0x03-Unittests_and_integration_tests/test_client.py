#!/usr/bin/env python3
"""
unit test for client.GithubOrgClient
"""
import unittest
from urllib.error import HTTPError
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, param, parameterized_class
from client import GithubOrgClient as GOC
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    '''test class that inherits from unittest'''

    @parameterized.expand([
        param(org='google'),
        param(org='abc'),
    ])
    @patch('client.get_json')
    def test_org(self, get_mock, org):
        '''
        test that GithubOrgClient.org returns the correct value
        '''
        goc = GOC(org)
        goc.org()
        get_mock.assert_called_once_with(
            'https://api.github.com/orgs/' + org
        )

    def test_public_repos_url(self):
        '''
        test that the result of _public_repos_url is the expected
        one based on the mocked payload
        '''
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = 'http://some_url'
            goc = GOC('test')
            self.assertEqual(goc._public_repos_url,
                             'http://some_url')
            mock_url.assert_called_once_with()

    @patch('client.get_json')
    def test_public_repos(self, get_mock):
        '''
        unit test for GithubOrgClient.public_repos
        '''
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:

            mock_url.return_value = 'http://some_url'
            get_mock.return_value = [
                {'name': 'google'}, {'name': 'abc'}
            ]
            goc = GOC('test')

            self.assertEqual(goc.public_repos(), ['google', 'abc'])
            mock_url.assert_called_once_with()
            get_mock.assert_called_once_with('http://some_url')

    @parameterized.expand([
        param(input_payload={'license': {'key': 'my_license'}},
              expected_license_key='my_license'),
        param(input_payload={'license': {'key': 'other_license'}},
              expected_license_key='other_license'),
    ])
    def test_has_license(self, input_payload, expected_license_key):
        '''
        unit test for GithubOrgClient.has_license
        '''
        goc = GOC('test')
        self.assertEqual(goc.has_license(
            input_payload, expected_license_key), True)


@parameterized_class(['org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'], TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''test class that inherits from unittest'''

    @classmethod
    def setUpClass(cls):
        '''
        class method called before tests in an individual class run
        '''
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload,
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        '''
        class method called after tests in an individual class have
        run
        '''
        cls.get_patcher.stop()

    def test_public_repos(self):
        '''
        test that GithubOrgClient.public_repos returns the correct
        list of repos
        '''
        goc = GOC('test')
        assert True

    def test_public_repos_with_license(self):
        '''
        test that GithubOrgClient.public_repos returns the correct
        list of repos that match the license
        '''
        goc = GOC('test')
        assert True


class HTTPError(Exception):
    """Exception raised for HTTP errors.

    Attributes:
        status_code -- the HTTP status code
        message -- the error message
    """

    def __init__(self, status_code, message):
        """Initialize the HTTPError instance.

        Args:
            status_code (int): The HTTP status code.
            message (str): The error message.
        """
        super().__init__(message)
        self.status_code = status_code
        self.message = message


if __name__ == '__main__':
    unittest.main()
