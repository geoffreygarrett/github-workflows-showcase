def get_upstream_dependencies(repo, dependencies, depth=-1):
    """
    :example:
        >>> example_dependencies = {
        ...     'A': ['B'],
        ...     'B': ['C'],
        ...     'C': ['D'],
        ...     'D': []
        ... }
        >>> get_upstream_dependencies('B', dependencies, -1)
        ['C', 'D']

    :example:
        >>> example_dependencies = {
        ...     'A': ['B'],
        ...     'B': ['C'],
        ...     'C': ['D'],
        ...     'D': []
        ... }
        >>> get_upstream_dependencies('B', example_dependencies, 1)
        ['C']


    :param repo:
    :param dependencies:
    :param depth:
    :return:
    """
    upstream = dependencies.get(repo, [])
    for dep in dependencies.get(repo, []):
        if depth > 0:
            depth -= 1
            if depth == 0:
                return upstream
            else:
                upstream.extend(get_upstream_dependencies(dep, dependencies, depth))
        else:
            upstream.extend(get_upstream_dependencies(dep, dependencies))
    return upstream


def get_downstream_dependencies(repo, dependencies, depth=-1):
    """
    :example:
        >>> example_dependencies = {
        ...     'A': ['B'],
        ...     'B': ['C'],
        ...     'C': ['D'],
        ...     'D': []
        ... }
        >>> get_downstream_dependencies('B', dependencies)
        ['A']

    :example:
        >>> example_dependencies = {
        ...     'A': ['B'],
        ...     'B': ['C'],
        ...     'C': ['D'],
        ...     'D': []
        ... }
        >>> get_downstream_dependencies('A', dependencies)
        []

    :example:
        >>> example_dependencies = {
        ...     'A': ['B'],
        ...     'B': ['C'],
        ...     'C': ['D'],
        ...     'D': []
        ... }
        >>> get_downstream_dependencies('C', dependencies)
        ['B', 'A']

    :example:
        >>> example_dependencies = {
        ...     'A': ['B'],
        ...     'B': ['C'],
        ...     'C': ['D'],
        ...     'D': []
        ... }
        >>> get_downstream_dependencies('C', dependencies, 1)
        ['B']

    :param repo:
    :param dependencies:
    :return:
    """
    downstream = []
    for repo_name, deps in dependencies.items():
        if repo in deps:
            downstream.append(repo_name)
            if depth > 0:
                depth -= 1
                if depth == 0:
                    return downstream
                else:
                    downstream.extend(get_downstream_dependencies(repo_name, dependencies, depth))
            else:
                downstream.extend(get_downstream_dependencies(repo_name, dependencies))
    return downstream


if __name__ == '__main__':
    import doctest

    doctest.testmod()
