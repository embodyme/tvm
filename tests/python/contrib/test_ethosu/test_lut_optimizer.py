# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Test the pass that removes unnecssary identity operation if the identity 
uses LUT and the preceding operator is LUT capable and doesn't already have a LUT.
"""
import pytest

pytest.importorskip("ethosu.vela")

import tvm
from tvm import relay
from tvm.relay.backend.contrib.ethosu.codegen import LUTsOptimizer
from . import infra


def test_merge_lut_into_conv():
    """If an operator that has a LUT attribute is followed by an identity operator
    with LUT, we can merge the two operataors."""

    ifm = relay.var("x", shape=(1, 8, 8, 4), dtype="int8")
    lut1 = relay.const([i for i in range(256)], dtype="int8")
    lut2 = relay.const([i for i in reversed(range(256))], dtype="int8")

    def before():
        conv1 = infra.make_ethosu_conv2d(ifm, 4, 4, (3, 3), (1, 1), (1, 1), (1, 1))
        id1 = infra.make_ethosu_identity(conv1, lut=lut1, activation="TANH")
        conv2 = infra.make_ethosu_conv2d(id1, 4, 7, (2, 2), (1, 1), (1, 1), (1, 1))
        id2 = infra.make_ethosu_identity(conv2, lut=lut2, activation="TANH")

        func = relay.Function(relay.analysis.free_vars(id2), id2)
        mod = tvm.IRModule.from_expr(func)
        return mod

    def after():
        conv1 = infra.make_ethosu_conv2d(
            ifm, 4, 4, (3, 3), (1, 1), (1, 1), (1, 1), lut=lut1, activation="TANH"
        )
        conv2 = infra.make_ethosu_conv2d(
            conv1, 4, 7, (2, 2), (1, 1), (1, 1), (1, 1), lut=lut2, activation="TANH"
        )

        func = relay.Function(relay.analysis.free_vars(conv2), conv2)
        mod = tvm.IRModule.from_expr(func)
        mod = relay.transform.InferType()(mod)
        return mod

    mod = LUTsOptimizer()(before())

    assert tvm.ir.structural_equal(mod, after())


def test_multiple_luts():
    """Test that when an operation already has a LUT, we don't overwrite that LUT"""

    ifm = relay.var("x", shape=(1, 8, 8, 4), dtype="int8")
    lut1 = relay.const([i for i in range(256)], dtype="int8")
    lut2 = relay.const([i for i in reversed(range(256))], dtype="int8")

    def before():
        conv1 = infra.make_ethosu_conv2d(ifm, 4, 4, (3, 3), (1, 1), (1, 1), (1, 1))
        id1 = infra.make_ethosu_identity(conv1, lut=lut1, activation="TANH")
        id2 = infra.make_ethosu_identity(id1, lut=lut2, activation="TANH")

        func = relay.Function(relay.analysis.free_vars(id2), id2)
        mod = tvm.IRModule.from_expr(func)
        return mod

    def after():
        conv1 = infra.make_ethosu_conv2d(
            ifm, 4, 4, (3, 3), (1, 1), (1, 1), (1, 1), lut=lut1, activation="TANH"
        )
        id2 = infra.make_ethosu_identity(conv1, lut=lut2, activation="TANH")

        func = relay.Function(relay.analysis.free_vars(id2), id2)
        mod = tvm.IRModule.from_expr(func)
        mod = relay.transform.InferType()(mod)
        return mod

    mod = LUTsOptimizer()(before())

    assert tvm.ir.structural_equal(mod, after())
