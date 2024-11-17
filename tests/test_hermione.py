# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import logging

from licomp.interface import Licomp
from licomp.interface import ObligationTrigger
from licomp.interface import ModifiedTrigger
from licomp.interface import CompatibilityStatus

from licomp_hermione.hermione import LicompHermione

lh = LicompHermione()

def test_supported():
    assert len(lh.supported_licenses()) > 60
    
def test_license_is_supported():
    assert lh.license_supported("BSD-3-Clause")
    
def test_license_is_not_supported():
    assert not lh.license_supported("Some-license-that-does-not-exist")
    
def test_trigger_is_supported():
    assert lh.trigger_supported(trigger=ObligationTrigger.BIN_DIST)
    
def test_trigger_is_not_supported():
    assert not lh.trigger_supported(trigger=ObligationTrigger.SNIPPET)
    
def test_compat():
    ret = lh.outbound_inbound_compatibility("GPL-2.0-only", "BSD-3-Clause", trigger=ObligationTrigger.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == "yes"
    assert ret['status'] == "success"

def test_incompat_1():
    ret = lh.outbound_inbound_compatibility("BSD-3-Clause", "GPL-2.0-only", trigger=ObligationTrigger.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == "no"
    assert ret['status'] == "success"

def test_incompat_2():
    ret = lh.outbound_inbound_compatibility("BSD-3-Clause", "GPL-2.0-only", trigger=ObligationTrigger.SNIPPET)
    logging.debug("ret: " + str(ret))
    assert ret['status'] == 'failure'

def test_incompat_3():
    ret = lh.outbound_inbound_compatibility("BSD-3-Clause", "DO_NO_EXIST", trigger=ObligationTrigger.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == None
    assert ret['status'] == "failure"

def test_incompat_4():
    ret = lh.outbound_inbound_compatibility("DO_NO_EXIST", "GPL-2.0-only", trigger=ObligationTrigger.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == None
    assert ret['status'] == "failure"

