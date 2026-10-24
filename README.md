# GitHubConnector

The `GitHubConnector` allows you to fetch organization members from GitHub using the REST API.

## Installation

Ensure you have the `integration-demo` library installed in your environment.

## Usage

```python
from integrations import GitHubConnector

# Initialize the connector
# Replace 'my-org' and 'your-github-token' with your actual credentials
connector = GitHubConnector(
    organization="my-org",
    token="your-github-token",
    timeout=15.0
)

# Fetch all members
try:
    users = connector.list_users()
    for user in users:
        print(f"User: {user.username}, Profile: {user.profile_url}")
except RuntimeError as e:
    print(f"Failed to fetch users: {e}")
```

## Configuration

- `organization`: The GitHub organization name (e.g., "python").
- `token`: A GitHub Personal Access Token with appropriate read permissions.
- `timeout`: Request timeout in seconds (default: 10.0).

## Security Note
Never hardcode your GitHub tokens in source code. Use environment variables or a secure secret management system to provide the `token` to the `GitHubConnector`.