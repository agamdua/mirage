from __future__ import absolute_import

from collections import Counter

import github3 as github

from .cred import GHEPW, PW
from .config import *  # noqa


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

    def get_issue_for_pull(self, pull):
        """Pass in the pull request **object**
        """
        return self.repo.issue(pull.number)

    def get_labels_on_pull(self, pull):
        return self.get_issue_for_pull(pull).iter_labels()

    def get_label_names(self, pull, labels):
        """pass in label objects"""
        return [ label.name for label in self.get_labels_on_pull ]

    def filter_pulls(self, assigned=False, state='open', label_name=None):
        """
        Returns a list based on filters

        Args:
            assigned (bool): assigned to nobody or assigned to somebody
                True returns all that are assigned
            state (str): 'all', 'open', 'closed' (mirroring github3 api)
        """
        filtered = []
        pull_filters = []
        label_filters = []
        issue_filters = []

        # TODO: filter by specific assignees
        if assigned:
            issue_filters.append(lambda x: x.assignee)
        else:
            issue_filters.append(lambda x: not x.assignee)

        if state != 'open':
            raise NotImplementedError(
                "Feel free to contribute to github.com/agamdua/mirage!"
            )

        if label_name:
            # TODO: support label name iterables
            if label_name.startswith('!'):
                label_filters.append(lambda x: x.name != label_name)
            else:
                label_filters.append(lambda x: x.name == label_name)

        for pull in self.pulls:
            for label_filter in label_filters:
                if filter(label_filter, self.get_labels_on_pull(pull)):
                    filtered.append(pull)

        final = []

        for index, pull in enumerate(filtered):
            for issue_filter in issue_filters:
                if issue_filter(pull):
                    final.append(pull)

        return final

    def get_assigned_count_l2(self, label_name=None, l2=True, l1=False):
        assignees = []
        if l1:
            assignees.extend(L1)
        if l2:
            assignees.extend(L2)

        assigned_count = Counter(
            pull.assignee
            for pull in self.filter_pulls(assigned=True, label_name='L2')
            if pull.assignee.login in assignees
        )
        return assigned_count

    def get_assigned_count_l1(self, label_name=None, l2=False, l1=True):
        """Yes, this is copied from a above. deal with it"""
        assignees = []
        if l1:
            assignees.extend(FIRST_REVIEWS)
        if l2:
            assignees.extend(L2)

        assigned_count = Counter(
            pull.assignee
            for pull in self.filter_pulls(assigned=True, label_name='!L2')
            if pull.assignee.login in assignees
        )
        return assigned_count

    def get_person_with_bad_luck_l1(self, label_name):
        assigned_count = self.get_assigned_count_l1(label_name)
        return min(assigned_count, key=assigned_count.get)

    def get_person_with_bad_luck_l2(self, label_name):
        assigned_count = self.get_assigned_count_l2(label_name)
        return min(assigned_count, key=assigned_count.get)

    def assign_things(self, level='L2'):
        unassigned_requests = self.filter_pulls(label_name=level)
        lower = level.lower()
        for pull in unassigned_requests:
            self.get_issue_for_pull(pull).assign(
                self.get_person_with_bad_luck_l2(level).login
            )
