# -*- coding: utf-8 -*-

import os
import json
import pickle
import csv


def make_dirs_for_file(pathname):
    try:
        os.makedirs(os.path.split(pathname)[0])
    except:
        pass


def exist(pathname, overwrite=False, display_info=True):
    def __path_type(pathname):
        if os.path.isfile(pathname):
            return 'File'
        if os.path.isdir(pathname):
            return 'Directory'
        if os.path.islink(pathname):
            return 'Symbolic Link'
        if os.path.ismount(pathname):
            return 'Mount Point'
        return 'Path'
    if os.path.exists(pathname):
        if overwrite:
            if display_info:
                print u'%s: %s exists. Overwrite.' % (__path_type(pathname), pathname)
            os.remove(pathname)
            return False
        else:
            if display_info:
                print u'%s: %s exists.' % (__path_type(pathname), pathname)
            return True
    else:
        if display_info:
            print u'%s: %s does not exist.' % (__path_type(pathname), pathname)
        return False


def load_text(pathname, display_info=True):
    if exist(pathname=pathname, display_info=display_info):
        with open(pathname, 'r') as f:
            return [line.strip() for line in f.readlines()]


def load_json(pathname, display_info=True):
    if exist(pathname=pathname, display_info=display_info):
        with open(pathname, 'r') as f:
            return json.load(f)


def dump_json(data, pathname, overwrite=False, display_info=True):
    make_dirs_for_file(pathname)
    if not exist(pathname=pathname, overwrite=overwrite, display_info=display_info):
        if display_info:
            print 'Write to file: %s' % pathname
        with open(pathname, 'w') as f:
            json.dump(data, f)


def load_model(pathname, display_info=True):
    if exist(pathname=pathname, display_info=display_info):
        with open(pathname, 'r') as f:
            return pickle.load(f)


def dump_model(model, pathname, overwrite=False, display_info=True):
    make_dirs_for_file(pathname)
    if not exist(pathname=pathname, overwrite=overwrite, display_info=display_info):
        if display_info:
            print 'Write to file: %s' % pathname
        with open(pathname, 'w') as f:
            pickle.dump(model, f)


def export_csv(data, fieldnames, pathname, overwrite=False, display_info=True):
    make_dirs_for_file(pathname)
    if not exist(pathname=pathname, overwrite=overwrite, display_info=display_info):
        if display_info:
            print 'Write to file: %s' % pathname
        with open(pathname, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            for row in data:
                writer.writerow(row)


def set_matplotlib_backend(backend=None):
    import matplotlib
    if matplotlib.get_backend() == 'MacOSX':
        matplotlib.use('TkAgg')
    if backend:
        matplotlib.use(backend)


def plot(args, backend=None):
    set_matplotlib_backend(backend=backend)
    import matplotlib.pyplot as plt
    plt.plot(*args)
    plt.show()


def semilogy(args, backend=None):
    set_matplotlib_backend(backend=backend)
    import matplotlib.pyplot as plt
    plt.semilogy(*args)
    plt.show()