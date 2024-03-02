import sys
import os


def linerize(collection):
    """

    :param collection: n-dimensional list or tuple
    :return: one-dimensional list
    """
    if collection == []:
        return []
    if not (isinstance(collection, list) or isinstance(collection, tuple)):
        return [collection]
    return linerize(collection[0]) + linerize(collection[1:])


def uri_from_path(path):
    try:
        root = sys._MEIPASS
        path = path.replace("../", '')
    except Exception:
        root = os.path.abspath('.')
    return os.path.join(root, path)
