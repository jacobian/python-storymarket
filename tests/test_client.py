"""
Tests for the parts of StorymarketClient not otherwise covered.
"""

import mock
import storymarket
import httplib2
from nose.tools import assert_raises

client = storymarket.StorymarketClient('APIKEY')

def test_json_encoding():
    mock_resp = httplib2.Response({"status": 200})
    mock_body = '{"hi": "there"}'
    mock_req = mock.Mock(return_value=(mock_resp, mock_body))

    with mock.patch('httplib2.Http.request', mock_req):
        client.request('/url/', 'POST', body={"hello": ["world"]})
        mock_req.assert_called_with(
            '%surl/' % client.BASE_URL,
            'POST', 
            body = '{"hello": ["world"]}',
            headers = {
                'Authorization': client.apikey,
                'Content-Type': 'application/json',
                'User-Agent': client.USER_AGENT,
            },
        )
        
def test_error_response():
    mock_resp = httplib2.Response({"status": 400})
    mock_body = 'oops!'
    mock_req = mock.Mock(return_value=(mock_resp, mock_body))
    
    with mock.patch('httplib2.Http.request', mock_req):
        assert_raises(storymarket.exceptions.StorymarketError, client.request, '/url/', 'GET')
            