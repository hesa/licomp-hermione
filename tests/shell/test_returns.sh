#!/bin/bash

# SPDX-FileCopyrightText: 2025 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

dummy_cli()
{
    PYTHONPATH=${PYTHONPATH}:. python3 licomp_hermione/__main__.py $*
}

check_ret()
{
    ACTUAL=$1
    EXPECTED=$2
    ARGS="$3"

    if [ $ACTUAL != $EXPECTED ]
    then
        echo " actual:\"$ACTUAL\" != expected:\"$EXPECTED\" :("
        echo "... try locally using:"
        echo "devel/licomp-hermione --local $ARGS ; echo \$?"
        exit 1
    fi
}

run_comp_test()
{
    EXP=$1
    shift
    dummy_cli $* > /dev/null 2>&1
    RET=$?
    printf "%-75s" "$*: "
    check_ret $RET $EXP "$*"
    echo "OK"
}

test_verify()
{
    # Success and compatible
    run_comp_test 0 "verify -il BSD-3-Clause -ol GPL-2.0-only"

    # Success and incompatible
    run_comp_test 2 "verify -il GPL-2.0-only -ol BSD-3-Clause"

    # Failure, since unsupported
    run_comp_test 5 "verify -il GPL-2.0-only -ol Unsupported"

    # Failure, since usecase unsupported
    run_comp_test 6 "--usecase snippet verify -il GPL-2.0-only -ol BSD-3-Clause"
    run_comp_test 6 "--usecase blabla  verify -il GPL-2.0-only -ol BSD-3-Clause"

    # Failure, since provisioning case unsupported
    run_comp_test 7 "--provisioning provide-webui verify -il GPL-2.0-only -ol BSD-3-Clause"
    run_comp_test 7 "--provisioning blabla        verify -il GPL-2.0-only -ol BSD-3-Clause"

    # add modification test once modification is implemented

    # check missing arguments
    run_comp_test 20 "verify"
    run_comp_test 20 "verify -il GPL-2.0-only"
    run_comp_test 20 "verify -ol GPL-2.0-only"
}

test_verify
