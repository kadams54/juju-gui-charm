#!/usr/bin/env python2
# -*- python -*-

# This file is part of the Juju GUI, which lets users view and manage Juju
# environments within a graphical interface (https://launchpad.net/juju-gui).
# Copyright (C) 2016 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License version 3, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import errno
import os

from charmhelpers.core.hookenv import (
    config as get_config,
    log,
)
from shelltoolbox import run

from backend import Backend
from utils import (
    config_json,
    log_hook,
)


def main():
    # Run pre-install tasks, if available.
    if os.path.isdir('exec.d'):
        dirnames = os.listdir('exec.d')
        dirnames.sort()
        for module in dirnames:
            filename = os.path.join('exec.d', module, 'charm-pre-install')
            try:
                run(filename)
            except OSError, e:
                # If the exec.d file does not exist or is not runnable or
                # is not a directory, assume we can recover.  Log the problem
                # and proceed.  Note that Juju Core has a special need of
                # errno.ENOTDIR because it apparently adds a ".empty" file in
                # empty charm directories, so trying to run
                # ./exec.d/.empty/charm-pre-install will trigger that error.
                if e.errno in (errno.ENOENT, errno.EACCES, errno.ENOTDIR):
                    log('{}: {}'.format(e.strerror, filename))
                else:
                    raise
    config = get_config()
    backend = Backend(config)
    backend.install()
    # Store current configuration.
    config_json.set(config)


if __name__ == '__main__':
    with log_hook():
        main()
