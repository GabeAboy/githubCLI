from github import GithubGateway, GithubRepository
from affinity import GithubPullRequestAuthorStats, GithubPullRequestStats

#Return an object of unique authors and their many reviewers
def mergeAuthorPullRequests(pullRequestsAndTheirReviewers):
    authors = {}
    for author in pullRequestsAndTheirReviewers:

        if author.author in authors:
            authors.get(author.author).add_pr(author)
        else:
            authors[author.author] = GithubPullRequestAuthorStats(author.reviewer)
    return authors

#Promt User for Repository and Ownername
#EX: GithubRepository(Owner,Repository)
#GithubRepository("expo", "expo-cli")
def userInput():
    userInput = {}
    while True:
        print "Press 0 to quit"

        repositoryTitle = raw_input("Enter a github repository title : ")
        # Condense these into one method
        if len(repositoryTitle) < 1:
            print "\nError: Please enter a repository title\n"
            continue
        if repositoryTitle == "0":
            print "You have terminated the CLI"
            break
        repositoryOwner = raw_input(
            "Enter the github repository owner username : ")
        if len(repositoryOwner) < 1:
            print "\nError: Please enter a repository title\n"
            continue
        if repositoryOwner == "0":
            print "You have terminated the CLI"
            break
        userInput["repOwner"] = repositoryOwner
        userInput["repoTitle"] = repositoryTitle
        return userInput

#Github OAuth
def authentication():
    print "Try logging in first"
    print "Or press 0 to opt out"
    while True:
        emailaddress = raw_input("Enter a github email address : ")
        if emailaddress == "0":
            print "You opt out\n"
            return GithubGateway('', '')
        token  = raw_input("Enter a github developer token or pres 0 to opt out: ")
        if token == "0":
            print "You opt out\n"
            return GithubGateway('','')
        gitGateway = GithubGateway(emailaddress, token)
        if gitGateway.authentication_status == 200:
            print "Welcome you logged in successfully"

            return gitGateway
        else:
            print "Try logging in again"    
def main():
    # Welcome introduction
    print "Welcome to the Github CLI"
    print "Given a github repository owner/id and a date range, we will scan for Pull Requests and print out:"
    print "\t- Pairwise affinity between the team members"
    print "\t- A team equity measurement"

    #Get user info
    gitGateway = authentication()
    while True:
        inputObj = userInput()
        
        #Create Git Repository instance
        requestedRepo = GithubRepository(inputObj.get('repOwner'), inputObj.get('repoTitle') )

        #TODO DELETE 7ffab3df49643defb2981e761bceb9807e3794b4
    
        #Retrieve all pull requests and its reviewers of the input repository
        pullRequestsAndTheirReviewers = gitGateway.get_pull_requests(
            requestedRepo)
        #Some authors create multiple pull requests, merge all pull requests for one unique author 
        authors = mergeAuthorPullRequests(pullRequestsAndTheirReviewers)
    
        #Create GithubPullRequestStats instance and all the pull requests
        githubPullRequestStats = GithubPullRequestStats()
        githubPullRequestStats.add_pr_list(pullRequestsAndTheirReviewers)

        print "\n\n\n\n"
        print "Affinity Scores:"
        for author, listOfAuthorReviewers in authors.items():
            print "\tAuthor: ", author
            print "\t\tReviewers: "
            for review in listOfAuthorReviewers.reviewerList:
                print "\t\t\t ", review, ": ", listOfAuthorReviewers.get_affinity(review)
        
        print "\n"
        print "Repository Team Equity Score: "
        print "\t",requestedRepo.repository_id,": ", githubPullRequestStats.get_team_equity()
        tryAgain = raw_input("Try another repo? 1=yes, 0=no: ")
        if tryAgain == "0":
            break
        
if __name__ == '__main__':
    main()
