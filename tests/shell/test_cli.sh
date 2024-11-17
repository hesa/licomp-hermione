#!/bin/bash

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

lh()
{
    PYTHONPATH=. ./licomp_hermione/__main__.py $*
    if [ $? -ne 0 ]
    then
        echo "failed: $*"
        exit 1
    fi
}

lh --help
lh --name
lh --version
lh supported-triggers
lh supported-licenses
lh verify -il MIT -ol BSD-3-Clause
