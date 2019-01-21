"""
Affinity tests.

Note that these tests assume a definition of affinity that may not be yours. Feel free to edit
those tests so they honor your definition but keeping the test intention.

"""
import unittest

from affinity import GithubPullRequestAuthorStats, GithubPullRequestStats
from github import PullRequest


class TestPairwiseAffinity(unittest.TestCase):
    def setUp(self):
        self.stats = GithubPullRequestAuthorStats()

    def test_empty(self):
        self.assertEqual(self.stats.get_affinity('someone'), 0)

    def test_half_split(self):
        self.stats.add_pr(PullRequest('alice', 'john'))
        self.stats.add_pr(PullRequest('alice', 'peter'))
        self.assertEqual(self.stats.get_affinity('john'), self.stats.get_affinity('peter'))


class TestTeamwiseEquity(unittest.TestCase):

    def _get_equity_for_pairs(self, *pairs):
        stats = GithubPullRequestStats()
        for author, reviewer in pairs:
            stats.add_pr(PullRequest(author, reviewer))
        return stats.get_team_equity()

    def test_empty(self):
        self.assertEqual(self._get_equity_for_pairs(), 1)

    def test_symmetric(self):
        self.assertEqual(self._get_equity_for_pairs(
            ('john', 'peter'),
            ('peter', 'john'),
        ), 1)

    def test_decrease_equity(self):
        initial = [
            ['john', 'peter'],
            ['john', 'peter'],
            ['nathan', 'john'],
        ]
        extra = initial + [['nathan', 'john']]
        self.assertGreater(
            self._get_equity_for_pairs(*initial),
            self._get_equity_for_pairs(*extra)
        )
