import json
import urllib.request
import urllib.error
from typing import List, Optional
from integrations.base import Connector, User

class GitHubConnector(Connector):
    def __init__(self, organization: str, token: str, timeout: float = 10.0):
        if not isinstance(organization, str) or not organization.strip():
            raise ValueError("Organization must be a non-empty string.")
        if not isinstance(token, str) or not token.strip():
            raise ValueError("Token must be a non-empty string.")
        
        self.organization = organization
        self.token = token
        self.timeout = timeout
        self.base_url = f"https://api.github.com/orgs/{organization}/members?per_page=100"

    def list_users(self) -> List[User]:
        users: List[User] = []
        next_url: Optional[str] = self.base_url

        while next_url:
            request = urllib.request.Request(next_url)
            request.add_header("Authorization", f"Bearer {self.token}")
            request.add_header("Accept", "application/vnd.github+json")

            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    data = json.loads(response.read().decode("utf-8"))
                    
                    for item in data:
                        users.append(User(
                            id=str(item["id"]),
                            username=item["login"],
                            profile_url=item["html_url"]
                        ))

                    # Handle pagination via Link header
                    link_header = response.headers.get("Link", "")
                    next_url = self._parse_next_link(link_header)

            except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
                raise RuntimeError(f"Failed to fetch users from GitHub: {e}")

        return users

    def _parse_next_link(self, link_header: str) -> Optional[str]:
        if not link_header:
            return None
        
        parts = link_header.split(",")
        for part in parts:
            if 'rel="next"' in part:
                return part.split(";")[0].strip("< >")
        return None