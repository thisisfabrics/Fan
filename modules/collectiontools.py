def linerize(collection):
    """

    :param collection: n-dimensional list or tuple
    :return: one-dimensional list
    """
    if not collection:
        return []
    if not (isinstance(collection, list) or isinstance(collection, tuple)):
        return [collection]
    return linerize(collection[0]) + linerize(collection[1:])

