import requests
import json
from requests.auth import HTTPBasicAuth


class PullRequest:
    """The information we care about a PR for calculating stats."""

    def __init__(self, author, reviewer, id):
        self.author = author
        self.reviewer = reviewer
        self.id = id

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
    def __init__(self, username, token):
        r = requests.get('https://api.github.com/user', auth=HTTPBasicAuth(username, token))
        self.authentication_status = r.status_code
        self.github_base_url = 'https://api.github.com'

    def get_pull_requests(self, repo):
        """
        :param GithubRepository repo:
        :param datetime.datetime date_from:
        :param datetime.datetime date_to:
        :return: sequence[GithubPullRequest]
        """
        response = requests.get('{}/repos/{}/{}/pulls'.format(self.github_base_url, repo.owner, repo.repository_id), dict(
            q='is:pr repo:{}/{} -review:none'.format(
                repo.owner, repo.repository_id),
            sort='created',
            direction='asc'
        )).json()

        pullRequestAndReviews = self.bind_pull_requests_to_reviews(repo, response)
        return pullRequestAndReviews
    
    #Joins pull requests and its associated reviews
    def bind_pull_requests_to_reviews(self, repo, response):
        listOfAllData = []
        
        #for all requests
        for pullrequest in response:
            revieweeLogin = []
            prID = pullrequest.get('number')
            ownerLogin = pullrequest.get('user').get('login')
            #get reviews
            reviewers = self.get_review_requests(repo, prID)
            #merge
            for reviewee in reviewers:
                revieweeLogin.append(reviewee.get('user').get('login'))
            listOfAllData.append(PullRequest(ownerLogin, revieweeLogin, prID))
        return listOfAllData

    #Gets PR reviews
    def get_review_requests(self, repo, prID):
        """
        :param GithubRepository repo:
        :param datetime.datetime date_from:
        :param datetime.datetime date_to:
        :return: sequence[GithubPullRequest]
        """
        reviewers = requests.get('{}/repos/{}/{}/pulls/{}/reviews'.format(self.github_base_url, repo.owner, repo.repository_id, prID), dict(
            q='is:pr repo:{}/{} -review:none'.format(repo.owner, repo.repository_id),
            sort='created',
            direction='asc'
        )).json()
        return reviewers
    
        
    # print json.dumps(response[0].base, sort_keys=True, indent=4,separators=(',',': '))
    # ... get from each pull request, its reviewer. note that the "reviewer" field is not always indicative
    # of who actually reviewed it (you'll see most "reviewed" PRs surprisingly have a null "reviewer".
    # For actually getting the reviewers, you'll have to fetch, for each PR, it's associated "review" objects.
    # ... beware of api limits when you're not authenticating github requests.
