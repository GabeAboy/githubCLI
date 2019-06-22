from itertools import permutations
"""
Affinity metrics definitions. Note that the classes written below are just a scaffold in order to be able to write
the sample tests. Feel free to completely rewrite this module as you see fit.
"""

"""Pairwise stats for a given author vs all it's reviewers."""
class GithubPullRequestAuthorStats:
    def __init__(self, reviewer):
        self.reviewerList = reviewer
        self.total_pull_requests = 1

    def add_pr(self, pr):
        self.total_pull_requests+=1
        if isinstance(pr.reviewer, str):
            self.reviewerList.append(pr.reviewer)
        else:
            self.reviewerList.extend(pr.reviewer)

    def get_affinity(self, reviewer):
        #Affinity score increases the more interactions you have with a given person
        #Increment by one for every occurance 
        return self.reviewerList.count(reviewer)

class GithubPullRequestStats:
    def __init__(self):
        self.pullrequests = []
    """Whole team stats"""
    def add_pr_list(self, prList):
        for pr in prList:
            self.add_pr(pr)
    def add_pr(self, pr):
        self.pullrequests.append(pr)

    def get_team_equity(self):
        listOfAllPeople = []
        numberOfCombinationsExisting = []
        penalty = 0
        #Gets a list of all unique participants
        #If the pr-review already exists, add to pentalty to be deucted later
        for pr in self.pullrequests:
            if pr not in numberOfCombinationsExisting:
                numberOfCombinationsExisting.append(pr)
            else:
                penalty+=1
            if pr.author not in listOfAllPeople and len(pr.author)>=1:
                listOfAllPeople.append(''.join(pr.author))
            if pr.reviewer not in listOfAllPeople and len(pr.reviewer)>=1:
                listOfAllPeople.append(''.join(pr.reviewer))
        #Get the number of permutations as an ideal equity
        #Deduct points for duplicates and PR-Reviews (one to many) that our 
        #API response returned
        
        #Idea, get max score and take away what the response returned thus negativily effecting
        #the equity
        #Additionally deduct a penalty for PRAuthor-Reviewer that happen more than once 
        perm = len(list(permutations(listOfAllPeople))) 
        return perm-len(numberOfCombinationsExisting)-penalty