import pytest
import json
import urllib.error
from unittest.mock import patch, MagicMock
from integrations.github import GitHubConnector
from integrations.base import User

def test_github_connector_init_validation():
    with pytest.raises(ValueError):
        GitHubConnector("", "token")
    with pytest.raises(ValueError):
        GitHubConnector("org", "")

@patch("urllib.request.urlopen")
def test_list_users_success(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps([
        {"id": 1, "login": "user1", "html_url": "https://github.com/user1"},
        {"id": 2, "login": "user2", "html_url": "https://github.com/user2"}
    ]).encode("utf-8")
    mock_response.headers = {}
    mock_urlopen.return_value.__enter__.return_value = mock_response

    connector = GitHubConnector("myorg", "mytoken")
    users = connector.list_users()

    assert len(users) == 2
    assert users[0] == User("1", "user1", "https://github.com/user1")
    assert users[1] == User("2", "user2", "https://github.com/user2")

@patch("urllib.request.urlopen")
def test_list_users_pagination(mock_urlopen):
    # Page 1
    resp1 = MagicMock()
    resp1.read.return_value = json.dumps([{"id": 1, "login": "u1", "html_url": "url1"}]).encode("utf-8")
    resp1.headers = {"Link": '<https://api.github.com/page2>; rel="next"'}
    resp1.__enter__.return_value = resp1
    
    # Page 2
    resp2 = MagicMock()
    resp2.read.return_value = json.dumps([{"id": 2, "login": "u2", "html_url": "url2"}]).encode("utf-8")
    resp2.headers = {}
    resp2.__enter__.return_value = resp2
    
    mock_urlopen.side_effect = [resp1, resp2]

    connector = GitHubConnector("myorg", "mytoken")
    users = connector.list_users()

    assert len(users) == 2
    assert users[0].username == "u1"
    assert users[1].username == "u2"
    assert mock_urlopen.call_count == 2

@patch("urllib.request.urlopen")
def test_list_users_http_error(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="http://test", code=401, msg="Unauthorized", hdrs={}, fp=None
    )
    connector = GitHubConnector("myorg", "mytoken")
    with pytest.raises(RuntimeError):
        connector.list_users()

@patch("urllib.request.urlopen")
def test_list_users_malformed_json(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = b"invalid json"
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    connector = GitHubConnector("myorg", "mytoken")
    with pytest.raises(RuntimeError):
        connector.list_users()

@patch("urllib.request.urlopen")
def test_list_users_empty(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps([]).encode("utf-8")
    mock_response.headers = {}
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    connector = GitHubConnector("myorg", "mytoken")
    assert connector.list_users() == []