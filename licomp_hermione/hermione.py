#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os

from licomp_hermione.config import module_name
from licomp_hermione.config import version

from licomp.interface import Licomp
from licomp.interface import ObligationTrigger
from licomp.interface import ModifiedTrigger
from licomp.interface import CompatibilityStatus

SCRIPT_DIR = os.path.dirname(__file__)
VAR_DIR = os.path.join(SCRIPT_DIR, 'var')

class LicompHermione(Licomp):

    def __init__(self):
        self.file_map = {
            ObligationTrigger.BIN_DIST: {
                ModifiedTrigger.UNMODIFIED: 'hermione-matrix-DistributionNonSource-Unmodified.json',
                ModifiedTrigger.MODIFIED: 'hermione-matrix-DistributionNonSource-Altered.json',
            },
            ObligationTrigger.SOURCE_DIST: {
                ModifiedTrigger.UNMODIFIED: 'hermione-matrix-DistributionSource-Unmodified.json',
                ModifiedTrigger.MODIFIED: 'hermione-matrix-DistributionSource-Altered.json',
            },
        }
        self.licenes_map = {
            ObligationTrigger.BIN_DIST: {
                ModifiedTrigger.UNMODIFIED: None,
                ModifiedTrigger.MODIFIED: None,
            },
            ObligationTrigger.SOURCE_DIST: {
                ModifiedTrigger.UNMODIFIED: None,
                ModifiedTrigger.MODIFIED: None,
            },
        }
        Licomp.__init__(self)
        self.triggers = [ObligationTrigger.BIN_DIST, ObligationTrigger.SOURCE_DIST]

        self.ret_statuses = {
            "yes": CompatibilityStatus.COMPATIBLE,
            "no": CompatibilityStatus.INCOMPATIBLE,
        }

    def name(self):
        return module_name

    def version(self):
        return version

    def __licenses_from_file(self,
                             trigger=ObligationTrigger.BIN_DIST,
                             modified=ModifiedTrigger.UNMODIFIED):
        if not self.licenes_map[trigger][modified]:
            filename = os.path.join(VAR_DIR, self.file_map[trigger][modified])
            with open(filename) as fp:
                data = json.load(fp)
                self.licenes_map[trigger][modified] = data['licenses']

        return self.licenes_map[trigger][modified]

    def supported_licenses(self):
        # we can check any of the files for the supported licenses
        return list(self.__licenses_from_file().keys())

    def supported_triggers(self):
        return self.triggers

    def _outbound_inbound_compatibility(self,
                                        outbound,
                                        inbound,
                                        trigger=ObligationTrigger.BIN_DIST,
                                        modified=ModifiedTrigger.UNMODIFIED):

        licenses = self.__licenses_from_file(trigger, modified)
        values = licenses[outbound][inbound]

        return self.outbound_inbound_reply(self.ret_statuses[values],
                                           f'values from matrix: {values}')
