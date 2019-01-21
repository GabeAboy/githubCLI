# ProfitWell Engineering Project

## Overview

Today you'll be working with the code in this repo to build a command line application in Python, with unit tests to assert the functionality. The tool will look at all Pull Requests for a given public Github repository and analyze the relationship between Pull Request authors and reviewers.

## Background

On a daily basis team members interact in various forms. Member interaction patterns will shape how knowledge is distributed within a team. We'd like to analyze those patterns and measure them.

Let's say, for the sake of the exercise, that team interaction happens pairwise. 
If a team is composed of John, Eric, Nathan and Todd, we could think of the team activity as a sequence of pairwise interactions:

 * (Nathan, Todd),
 * (Nathan, Eric),
 * (Eric, John),
 * (Nathan, Todd)
 
 In this case, Nathan seems more likely to interact with Todd than Eric.
 We'd like to quantify that relationship by introducing two metrics: **Pairwise Affinity** and **Team Equity**


### Pairwise Affinity

For a given team member, their affinity with another member measures how often they interact, relative to how often they interact with other team members.

This means, in the example above, affinity between Nathan and Todd is higher than between Nathan and Eric.

Pairwise affinity then should always hold: If A interacts with B more times than it does with C, `affinity(A,B) > affinity(A,C)`

This definition is purposely loose. We'd like you to define a pairwise affinity metric.

### Team Equity
   
In a team that interacts pairwise, it's equity measures how homogenous are those interactions. 

In the previous example, there seems to bee too much activity between Nathan and Todd. The team equity would be higher if, for example, the last interaction was between Nathan and John.

Also this definition is meant to be properly defined by you.

Notice that there's not a single perfect definition for these. Soon you'll realize there's many ways of defining them. It's important that you are able to explain what criteria you have considered in order to arrive at these definitions.
  
  
## Exercise

In this repo you've been provided with a python skeleton project with some unit tests and a lot of room for you to elaborate. You can leverage the code you see here, but don't be afraid to rewrite anything as you see fit.

The software you write will be a command line tool that, given a github repository owner/id and a date range, will scan for Pull Requests and print out:

- Pairwise affinity between the team members
- A team equity measurement

Don't worry too much about the exact metric that you use to determine pairwise affinity and team equity. The focus will be much more around the code you write and your approach to the problem than it is on whether or not you selected the best mathematical model for solving the problem.


### Deliverables

- The working tool, as a runnable command line application
- Tests
- Documentation on as many aspects as you see fit.


## Help

### Setup a Virtual Env and Install the Requirements

```bash
mkvirtualenv affinity-project
pip install -r requirements.txt
```

### Run the Tests

There are a couple tests already setup, which will fail. You can run the failing tests by running the following commands:

```bash
python -m unittest src/test_affinity.py
```

You can run individual test methods using the following syntax:

```bash
python -m unittest <test_filename.py>.<classname>.<method_name>
```

### Library Documentation

There are a few key libraries this project is using. You can find the documentation for them below:

  * [requests](http://docs.python-requests.org/en/master/)
  * [nose](https://nose.readthedocs.io/en/latest/)

