#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os

from licomp_hermione.config import module_name
from licomp_hermione.config import module_url
from licomp_hermione.config import original_data_url
from licomp_hermione.config import version
from licomp_hermione.config import disclaimer
from licomp_hermione.config import supported_api_version

from licomp.interface import Licomp
from licomp.interface import Provisioning
from licomp.interface import UseCase
from licomp.interface import Modification
from licomp.interface import CompatibilityStatus

SCRIPT_DIR = os.path.dirname(__file__)
VAR_DIR = os.path.join(SCRIPT_DIR, 'data')

class LicompHermione(Licomp):

    def __init__(self):
        self.file_map = {
            Provisioning.BIN_DIST: {
                Modification.UNMODIFIED: 'hermione-matrix-DistributionNonSource-Unmodified.json',
                Modification.MODIFIED: 'hermione-matrix-DistributionNonSource-Altered.json',
            },
            Provisioning.SOURCE_DIST: {
                Modification.UNMODIFIED: 'hermione-matrix-DistributionSource-Unmodified.json',
                Modification.MODIFIED: 'hermione-matrix-DistributionSource-Altered.json',
            },
            Provisioning.LOCAL_USE: {
                Modification.UNMODIFIED: 'hermione-matrix-InternalUse-Unmodified.json',
                Modification.MODIFIED: 'hermione-matrix-InternalUse-Altered.json',
            },
        }
        self.licenes_map = {
            Provisioning.BIN_DIST: {
                Modification.UNMODIFIED: None,
                Modification.MODIFIED: None,
            },
            Provisioning.SOURCE_DIST: {
                Modification.UNMODIFIED: None,
                Modification.MODIFIED: None,
            },
            Provisioning.LOCAL_USE: {
                Modification.UNMODIFIED: None,
                Modification.MODIFIED: None,
            },
        }
        Licomp.__init__(self)
        self.provisionings = [Provisioning.BIN_DIST, Provisioning.SOURCE_DIST, Provisioning.LOCAL_USE]
        self.usecase = [UseCase.LIBRARY]
        self.ret_statuses = {
            "yes": CompatibilityStatus.COMPATIBLE,
            "no": CompatibilityStatus.INCOMPATIBLE,
        }

    def name(self):
        return module_name

    def version(self):
        return version

    def url(self):
        return module_url

    def data_url(self):
        return original_data_url

    def disclaimer(self):
        return disclaimer

    def __licenses_from_file(self,
                             provisioning=Provisioning.BIN_DIST,
                             modification=Modification.UNMODIFIED):
        if not self.licenes_map[provisioning][modification]:
            filename = os.path.join(VAR_DIR, self.file_map[provisioning][modification])
            with open(filename) as fp:
                data = json.load(fp)
                self.licenes_map[provisioning][modification] = data['licenses']

        return self.licenes_map[provisioning][modification]

    def supported_licenses(self):
        # we can check any of the files for the supported licenses
        return list(self.__licenses_from_file().keys())

    def supported_provisionings(self):
        return self.provisionings

    def supported_usecases(self):
        return self.usecase

    def supported_api_version(self):
        return supported_api_version

    def _outbound_inbound_compatibility(self,
                                        outbound,
                                        inbound,
                                        usecase,
                                        provisioning=Provisioning.BIN_DIST,
                                        modification=Modification.UNMODIFIED):

        licenses = self.__licenses_from_file(provisioning, modification)
        values = licenses[outbound][inbound]

        return self.outbound_inbound_reply(self.ret_statuses[values],
                                           f'values from matrix: {values}')
