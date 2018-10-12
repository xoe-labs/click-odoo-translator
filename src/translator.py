#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is part of the click-odoo-translator (R) project.
# Copyright (c) 2018 ACSONE SA/NV and XOE Corp. SAS
# Authors: Stéphane Bidoul, Thomas Binsfeld, Benjamin Willig, David Arnold, et al.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, see <http://www.gnu.org/licenses/>.
#

import logging

import click
import click_odoo

# from click_odoo import odoo

# from utils import manifest, gitutils

_logger = logging.getLogger(__name__)

# --------- INSTRUCTIONS --------------
# Start building the CLI around main()
# The click-context is enriched to env,
# which behaves like an odoo's self.env
# You might have a look at an example
# click-odoo pproject to get familiar.
# Also, don't forget to consult click's
# excellent docs.
# -------------------------------------

def main(env):
    """ Main description of the command.
    """
    pass


if __name__ == '__main__':  # pragma: no cover
    main()
