from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import os

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TRANSACTION_PATH='/v3/transactions/delivery/search'
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# Defaults for our simple example.
DEFAULT_TERM = 'chinese'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 10


def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token


def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def transaction_search(bearer_token, location):
    """Query the Transactio API by a location.
    Args:
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """
    url_params = {'location': location.replace(' ', '+')}
    print(location.replace(' ', '+'))

    return request(API_HOST,TRANSACTION_PATH,bearer_token,url_params=url_params)

def search(bearer_token, term, offset, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'offset': offset
    }

    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def get_business(bearer_token, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, bearer_token)

def query_api(location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    #bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)
    bearer_token ='SHdrjUqMJXqXBKUc7bGIplM8y6tnbwZbXXDbWPCd9wWMP8tX9PdJrC5MZHwJRhb7jMtLjXxT-hsWjNf2OkdiDWd30HsS84AVI5iRnrpxkak3HbWXAdUKvraQ_wgXWXYx'
    response =  transaction_search(bearer_token,location)
    response = response.get('businesses')
    return response

def main():
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    #bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)
    bearer_token ='SHdrjUqMJXqXBKUc7bGIplM8y6tnbwZbXXDbWPCd9wWMP8tX9PdJrC5MZHwJRhb7jMtLjXxT-hsWjNf2OkdiDWd30HsS84AVI5iRnrpxkak3HbWXAdUKvraQ_wgXWXYx'
    response =  transaction_search(bearer_token, '1910 Entrepreneur Dr, Raleigh, NC 27518')
    response = response.get('businesses')
    print(json.dumps(response, indent=4))

if __name__ == '__main__':
    main()
