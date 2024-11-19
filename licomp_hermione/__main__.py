#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from licomp.interface import Provisioning
from licomp.interface import UseCase
from licomp.main_base import LicompParser

from licomp_hermione.config import cli_name
from licomp_hermione.config import description
from licomp_hermione.config import epilog
from licomp_hermione.hermione import LicompHermione

def main():
    lh = LicompHermione()
    o_parser = LicompParser(lh,
                            cli_name,
                            description,
                            epilog,
                            UseCase.LIBRARY,
                            Provisioning.BIN_DIST)
    o_parser.run()


if __name__ == '__main__':
    main()
