import unittest

from github import GithubRepository, GithubGateway, PullRequest


class TestGithubEndToEnd(unittest.TestCase):
    def setUp(self):
        self.gateway = GithubGateway(username='your-username',
                                     password='get-token')

    def test_facebook_openr(self):
        repo = GithubRepository(owner='facebook', repository_id='openr')
        pull_requests = list(self.gateway.get_pull_requests(repo))
        self.assertEqual(len(pull_requests), 4)
        #TODO: can you assert not just on the length but more explicitly?

    def test_large_repo(self):
        repo = GithubRepository(owner='Microsoft', repository_id='TypeScript')
        pull_requests = list(self.gateway.get_pull_requests(repo))
        #TODO: can you assert not just on the length but more explicitly?
        self.assertEqual(len(pull_requests), 30)
