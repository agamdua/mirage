def filter_by_label(label_names=None):
    """Returns a list of callables that can be applied as label filters

    Supports (limited) querying.

    Example:
        label_names = ['mylabel', '!not-my-label']

        will get the pull requests with `mylabel`, but not the ones
        with `not-my-label`
    """
    label_filters = []

    for label in label_names:
        if label.startswith('!'):
            label_filters.append(lambda x: x.name != label)
        else:
            label_filters.append(lambda x: x.name == label)

    return label_filters


def filter_pulls(pulls, assigned=None, state='open', labels=None):
    """
    Returns a list based on filters

    Args:
        pulls (iterable of pull request objects)
        assigned (bool or None): assigned to nobody or assigned to somebody
            True returns all that are assigned
        state (str): 'all', 'open', 'closed' (mirroring github3 api)
        labels (iterable)

    TODOs:
        - assigned needs to support specific assignees
        - only supports open pull requests
    """
    filtered = []
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

    if labels:
        label_filters = filter_by_label(labels)

    for pull in pulls:


    # TODO: need to confirm this works with all filters
    for pull in pulls:
        for label_filter in label_filters:
            if filter(label_filter, pull.issue().iter_labels()):
                continue
        filtered.append(pull)

    final = []

    for index, pull in enumerate(filtered):
        for issue_filter in issue_filters:
            if issue_filter(pull):
                final.append(pull)

    return final
