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

# import mock
import os
import subprocess

import click
import click_odoo
from click.testing import CliRunner
# from click_odoo import odoo

from src.translator import main

# from ..utils import manifest, gitutils

# this extends the addons path of the odoodb and odoocfg fixtures
test_addons_dir = os.path.join(
    os.path.dirname(__file__), 'data', 'test_translator')


def test_translator_base(odoodb, odoocfg, tmpdir):
    addon_name = 'addon_test_translator'
    addon_path = os.path.join(test_addons_dir, addon_name)
    i18n_path = os.path.join(addon_path, 'i18n')
    pot_filepath = os.path.join(i18n_path, addon_name + '.pot')

    subprocess.check_call([
        click_odoo.odoo_bin,
        '-d', odoodb,
        '-c', str(odoocfg),
        '-i', addon_name,
        '--stop-after-init',
    ])

    if os.path.exists(pot_filepath):
        os.remove(pot_filepath)

    result = CliRunner().invoke(main, [
        '-d', odoodb,
        '-c', str(odoocfg),
        '--addons-dir', test_addons_dir,
    ])

    assert result.exit_code == 0
    assert os.path.isdir(i18n_path)
    assert os.path.isfile(pot_filepath)
    with open(pot_filepath) as f:
        assert 'myfield' in f.read()


def test_translator_msgmerge(odoodb, odoocfg, tmpdir):
    addon_name = 'addon_test_translator'
    addon_path = os.path.join(test_addons_dir, addon_name)
    i18n_path = os.path.join(addon_path, 'i18n')
    pot_filepath = os.path.join(i18n_path, addon_name + '.pot')
    fr_filepath = os.path.join(i18n_path, 'fr.po')

    subprocess.check_call([
        click_odoo.odoo_bin,
        '-d', odoodb,
        '-c', str(odoocfg),
        '-i', addon_name,
        '--stop-after-init',
    ])

    if not os.path.exists(i18n_path):
        os.makedirs(i18n_path)
    if os.path.exists(pot_filepath):
        os.remove(pot_filepath)
    # create empty fr.po, that will be updated by msgmerge
    with open(fr_filepath, 'w'):
        pass
    assert os.path.getsize(fr_filepath) == 0

    result = CliRunner().invoke(main, [
        '-d', odoodb,
        '-c', str(odoocfg),
        '--addons-dir', test_addons_dir,
        '--msgmerge',
    ])

    assert result.exit_code == 0
    assert os.path.getsize(fr_filepath) != 0
    with open(fr_filepath) as f:
        assert 'myfield' in f.read()


def test_translator_msgmerge_if_new_pot(odoodb, odoocfg, tmpdir):
    addon_name = 'addon_test_translator'
    addon_path = os.path.join(test_addons_dir, addon_name)
    i18n_path = os.path.join(addon_path, 'i18n')
    pot_filepath = os.path.join(i18n_path, addon_name + '.pot')
    fr_filepath = os.path.join(i18n_path, 'fr.po')

    subprocess.check_call([
        click_odoo.odoo_bin,
        '-d', odoodb,
        '-c', str(odoocfg),
        '-i', addon_name,
        '--stop-after-init',
    ])

    if not os.path.exists(i18n_path):
        os.makedirs(i18n_path)
    if os.path.exists(pot_filepath):
        os.remove(pot_filepath)
    # create empty .pot
    with open(pot_filepath, 'w'):
        pass
    # create empty fr.po
    with open(fr_filepath, 'w'):
        pass
    assert os.path.getsize(fr_filepath) == 0

    result = CliRunner().invoke(main, [
        '-d', odoodb,
        '-c', str(odoocfg),
        '--addons-dir', test_addons_dir,
        '--msgmerge-if-new-pot',
    ])

    assert result.exit_code == 0
    # po file not changed because .pot did exist
    assert os.path.getsize(fr_filepath) == 0

    # now remove pot file so a new one will
    # be created and msgmerge will run
    os.remove(pot_filepath)

    result = CliRunner().invoke(main, [
        '-d', odoodb,
        '-c', str(odoocfg),
        '--addons-dir', test_addons_dir,
        '--msgmerge-if-new-pot',
    ])

    with open(fr_filepath) as f:
        assert 'myfield' in f.read()
