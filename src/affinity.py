"""
Affinity metrics definitions. Note that the classes written below are just a scaffold in order to be able to write
the sample tests. Feel free to completely rewrite this module as you see fit.
"""

class GithubPullRequestAuthorStats:
    """Pairwise stats for a given author vs all it's reviewers."""
    def __init__(self):
        self.by_reviewer = {}
        self.total_pull_requests = 0

    def add_pr(self, pr):
        # TODO: implement
        pass

    def get_affinity(self, reviewer):
        # TODO: all yours
        pass


class GithubPullRequestStats(object):
    """Whole team stats"""

    def add_pr(self, pr):
        # TODO: implement
        pass

    def get_team_equity(self):
        # TODO: implement
        pass
