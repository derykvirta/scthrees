""" A wrapper around Pro Basketball API """

import json
import requests
import urllib

import constants


class PBAClient:
  def search_player(self, first_name='', last_name=''):
    self._request_params = {
      'first_name': first_name,
      'last_name': last_name
    }
  
    url = self._build_url(constants.PBA_PLAYER_BASIC)
    results = self._request(url)

    # Make sure we get the right player.
    # Find the player in the list by a match on the full name.
    name_search_term =  ' '.join([first_name, last_name]).strip()
    player_dict = next(r for r in results if name_search_term in r['player_name'].lower())
    print player_dict
  
  def _request(self, url, payload=None, method='post'):
    """ Send request to Pro Basketball API.

    Default method to post since most of the remote API endpoints require post.
    """
    r = requests.get(url) if method == 'get' else requests.post(url, data=json.dumps(payload))

    # Response, status etc
    return json.loads(r.text)
  
  def _build_url(self, base_url):
    # Clean up none values from request params.
    self._request_params.update((k, v) for k, v in self._request_params.iteritems() if v is not None)
  
    # Add the api key.
    self._request_params.update({'api_key': constants.PBA_API_KEY})
  
    # Now create the whole URL.
    return '%s?%s' % (base_url, urllib.urlencode(self._request_params))
