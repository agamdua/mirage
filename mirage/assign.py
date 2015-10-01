from __future__ import absolute_import

from collections import Counter

import github3 as github
import six

from terminaltables import AsciiTable

from .cred import GHEPW, PW
from .config import *  # noqa
from .query import filter_pulls


class Repo(object):
    def __init__(self, username, repo):
        """
        Args:
            username (str): 'username'
            repo (str): in the format of '<organization>/<repo>'
        """
        self.gh = github.GitHubEnterprise(GHE)
        # self.gh = github.login(username, PW)
        self.user = self.gh.login(username, GHEPW)
        self.repo = self.gh.repository(*repo.split('/'))


def get_reviewer_workload(pulls, reviewers):
    reviewer_workload = Counter(
        pull.assignee.login for pull in pulls
    )
    reviewer_workload.update({person: 0 for person in reviewers})

    return reviewer_workload


def get_reviewer(reviewer_workload, weights=None):
    if weights is not None:
        raise NotImplementedError(
            "Feel free to contribute to github.com/agamdua/mirage!"
        )

    return reviewer_workload.most_common()[-1][0]


def display_pull_stats(reviewers, reviewer_workload):
    table_data = [
        ['Assignee', '# assigned'],
    ]

    total = 0
    for reviewer in reviewers:
        workload = reviewer_workload[reviewer]
        table_data.append(
            [reviewer, six.text_type(workload)]
        )
        total += workload

    table_data.append(['=====================', '=='])
    table_data.append(['TOTAL: ', six.text_type(total)])

    table = AsciiTable(table_data)
    print(table.table)


def assign_pulls(repo, labels, reviewers, verbose=True):
    """
    Assigns pull requests on github to reviewers

    Args:
        - pulls (list of pull request obj)
        - labels (list of str): label names with query syntax supported
        - reviewers (list of str): reviewer github usernames
    """
    if not verbose:
        raise NotImplementedError(
            "Feel free to contribute to github.com/agamdua/mirage!"
        )

    unassigned_pulls = filter_pulls(
        repo, repo.repo.iter_pulls(), labels=labels, assigned=False
    )

    if not unassigned_pulls:
        print("\n\nNothing to assign for labels: {}".format(labels))

    # TODO: download all pull objects and cache them and run the
    # queries on that
    assigned_pulls = filter_pulls(
        repo, repo.repo.iter_pulls(), labels=[], assigned=True
    )

    reviewer_workload = get_reviewer_workload(assigned_pulls, reviewers)

    for pull in unassigned_pulls:
        reviewer = get_reviewer(reviewer_workload)
        repo.repo.issue(pull.number).assign(reviewer)
        print("Assigned {} to pull request: {}".format(reviewer, pull.number))
        reviewer_workload[reviewer] += 1

    display_pull_stats(reviewers, reviewer_workload)

