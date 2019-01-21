import requests
from requests.auth import HTTPBasicAuth


class PullRequest:
    """The information we care about a PR for calculating stats."""
    def __init__(self, author, reviewer):
        self.author = author
        self.reviewer = reviewer

    def __eq__(self, other):
        return (
            isinstance(other, PullRequest) and
            self.author == other.author and
            self.reviewer == other.reviewer
        )

    def __repr__(self):
        return 'PullRequest({}, {})'.format(repr(self.author), repr(self.reviewer))


class GithubRepository:
    """The information we need about a github respository in order to fetch PRs from it."""
    def __init__(self, owner, repository_id):
        self.owner = owner
        self.repository_id = repository_id


class GithubGateway:
    def __init__(self, username, password):
        self.auth = HTTPBasicAuth(username, password)
        self.github_base_url = 'https://api.github.com'

    def get_pull_requests(self, repo):
        """
        :param GithubRepository repo:
        :param datetime.datetime date_from:
        :param datetime.datetime date_to:
        :return: sequence[GithubPullRequest]
        """
        response = requests.get('{}/search/issues'.format(self.github_base_url), dict(
            q='is:pr repo:{}/{} -review:none'.format(repo.owner, repo.repository_id),
            sort='created',
            direction='asc'
        )).json()

        # ... get from each pull request, its reviewer. note that the "reviewer" field is not always indicative
        # of who actually reviewed it (you'll see most "reviewed" PRs surprisingly have a null "reviewer".
        # For actually getting the reviewers, you'll have to fetch, for each PR, it's associated "review" objects.
        # ... beware of api limits when you're not authenticating github requests.
