import json

TRACKED_API_URL = 'https://www.trackedhq.com/api/v2/'


# noinspection PyMethodMayBeStatic
class Resource:
    def __init__(self, api):
        self._api = api
        self._session = api.session

    def _get_returned(self, response):
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return response.text

    def _get(self, url):
        response = self._session.get(self._getURL(url))
        return self._get_returned(response)

    def _post(self, url, data):
        response = self._session.post(self._getURL(url), data)
        return self._get_returned(response)

    def _put(self, url, data):
        response = self._session.put(self._getURL(url), data)
        return self._get_returned(response)

    def _delete(self, url):
        response = self._session.delete(self._getURL(url))
        return self._get_returned(response)

    # ==============================================================
    # Helper functions
    # ==============================================================
    def _getURL(self, url):
        credentials = ("&" if "?" in url else "?") + \
                      "email_address=" + self._api.email_address + \
                      "&api_token=" + self._api.api_token
        new_url = TRACKED_API_URL + str(self._api.basecamp_account_id) + url + credentials
        return new_url
