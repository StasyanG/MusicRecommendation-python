""" Utility functions """

import urllib.request

def get_request(url, parameters=None, headers=None):
    """
    Overview
    ----------
    Calls URL (GET request) and returns response data

    Parameters
    ----------
    url (string):
        URL to call
    parameters (dict):
        Request parameters
    headers (dict):
        Request headers

    Returns
    ----------
    result:
        Response data
    """
    # Construct param string
    param_string = ''
    if parameters is not None:
        for param_name, param_value in parameters.items():
            if len(param_string) is 0:
                param_string += '?'
            else:
                param_string += '&'
            param_string += param_name + '=' + urllib.request.quote(param_value)
    # Add headers
    request = urllib.request.Request(url + param_string)
    if headers is not None:
        for header_name, header_value in headers.items():
            if header_name is not '' and header_value is not '':
                request.add_header(header_name, header_value)
    # Get result
    result = None
    try:
        with urllib.request.urlopen(request) as response:
            result = response.read()
    except urllib.request.HTTPError as err:
        print('Could not access the page ' + request.full_url + ' (', err.code, ')')
    return result

def ascii_string(string):
    """
    Overview
    ----------
    Return a string with spaces in places of non-ascii characters

    Parameters
    ----------
    string (string):
        String to filter

    Returns
    ----------
    (string):
        String without non-ascii characters
    """
    return ''.join([i if ord(i) < 128 else ' ' for i in string])

