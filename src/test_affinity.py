import unittest
from affinity import GithubPullRequestAuthorStats, GithubPullRequestStats
from github import PullRequest

"""
Affinity tests.

Note that these tests assume a definition of affinity that may not be yours. Feel free to edit
those tests so they honor your definition but keeping the test intention.

"""

# GithubPullRequestAuthorStats()
class TestPairwiseAffinity(unittest.TestCase):
    def setUp(self):
        # TODO Make sure that these tests reflect the implementation that is the datastructure
        # TODO is this the proper datastructure list of reviewers
        self.stats = GithubPullRequestAuthorStats(["Gabe", "Monica"])
        self.thing = {
            "John": self.stats
        }
    def test_empty(self):
        self.assertEqual(self.stats.get_affinity('someone'), 0)

    def test_half_split(self):
        self.stats.add_pr(PullRequest('alice', 'john', 1))
        self.stats.add_pr(PullRequest('alice', 'peter', 2))
        self.assertEqual(self.stats.get_affinity('john'),
                         self.stats.get_affinity('peter'))
    def test_major_affinity(self):
        self.stats.add_pr(PullRequest('Nathan', 'Todd', 1))
        self.stats.add_pr(PullRequest('Nathan', 'Eric', 2))

        self.stats.add_pr(PullRequest('Eric', 'John', 3))
        self.stats.add_pr(PullRequest('Nathan', 'Todd', 4))
        # The scores return the same
        self.assertGreater(self.stats.get_affinity('Todd'),
                         self.stats.get_affinity('Eric'))

    def test_string_list_affinity(self):
                                    #Author, Reviewer, pullrequest ID
        self.stats.add_pr(PullRequest('Nathan', ['Todd','Eric'], 1))
        self.stats.add_pr(PullRequest('Nathan', 'Eric', 2))

        self.stats.add_pr(PullRequest('Eric', 'John', 3))
        self.stats.add_pr(PullRequest('Nathan', 'Eric', 4))
        self.assertEqual(self.stats.get_affinity('Eric'),3)


class TestTeamwiseEquity(unittest.TestCase):
    def _get_equity_for_pairs(self, *pairs):
        stats = GithubPullRequestStats()
        for author, reviewer in pairs:
            stats.add_pr(PullRequest(author, reviewer, 1))
        return stats.get_team_equity()

    def test_empty(self):
        self.assertEqual(self._get_equity_for_pairs(), 1)

    def test_symmetric(self):
        self.assertEqual(self._get_equity_for_pairs(
            ('john', 'peter'),
            ('peter', 'john'),
        ), 0)

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
