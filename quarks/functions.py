#!python

""" Define the Quarks module """

import os
import pprint


def rget(dict_object, path_list):
    """ Returns the value of the item at the end of `path_list`

    All this does is safely handle a KeyError in the event that it is raised
    during a `reduce(lambda)` operation.

    @param dict_object: a python dictionary to search.  
    @param path_list: a list of strings representing the path to the 
    desired object
    @returns: the value found at the provided path or the original
    object if there is a KeyError

    td = {'a' :['A', 'B', 'C'], 'b' : {'foo': 1, 'bar': 2, 'baz': 3}}
    print rget(td, ['b', 'baz'])
    >>> 3

    TODO: I'm not a fan of the return value.  It works, but I think I would
    prefer to determine some other rational response.
    """
    try:
        return reduce(lambda d, k: d[k], path_list, dict_object)
    except KeyError:
        return dict_object

def map_path(path, filters=[]):
    """ Returns a dictionary representation of a filesystem 

    @returns: a dictionary mapping of the filesystem where folders are
    represented with keys as the folder name and the value will be a dictionary
    of that folder's contents.  Files have their filename as a key and `None`
    for a value

    my_home = map_path('~/')
    print my_home
    >>> {'bin': {...},                  # folder
         'Documents': {...},            # linked folder (same as a normal one)
         'docker-compose.yaml': None}   # file

    TODO: I'd like to do something more useful with the value for files.  Assuming
    that a user may have access to one of these dictionaries, we should support:
        with open(my_filesystem['readme.md']) as readme_file:
            ...
    So that file access can be as easy as pathfinding.  For now, that remains
    beyond the scope of my present need.
    """

    def _internal(arg, path, names):
        path_list = path.split('/')
        target = rget(arg, path_list[:-1])
        target[path_list[-1]] = {name: "{}/{}".format(path, name) for name in names}
        return target

    result = {}
    os.path.walk(path, _internal, result)
    return result

    










