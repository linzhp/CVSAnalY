#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 University of California, Santa Cruz
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Author:
#       Zhongpeng Lin <linzhp@soe.ucsc.edu>

import unittest
from pycvsanaly2.extensions.Metrics import JavaComplexityCalculator
import plyj.parser as plyj

class JavaComplexityTest(unittest.TestCase):
    parser = plyj.Parser()

    def test_arbitrary_method_visit(self):
        visitor = JavaComplexityCalculator()
        self.assertTrue(visitor.visit_AnyNode("any node"))
        with self.assertRaises(AttributeError):
            visitor.do_something("else")

    def test_visit_ConstructorDeclaration(self):
        tree = self.parser.parse_string('class Foo { Foo() {} }')
        visitor = JavaComplexityCalculator()
        tree.accept(visitor)
        self.assertListEqual([1], visitor.mccabe_values)

    def test_visit_MethodDeclaration(self):
        tree = self.parser.parse_string('class Foo { void bar() {} }')
        visitor = JavaComplexityCalculator()
        tree.accept(visitor)
        self.assertListEqual([1], visitor.mccabe_values)

    def test_visit_Throws(self):
        tree = self.parser.parse_string('class Foo { void bar() throws Exception {} }')
        visitor = JavaComplexityCalculator()
        tree.accept(visitor)
        self.assertListEqual([2], visitor.mccabe_values)

    def test_visit_Conditional(self):
        tree = self.parser.parse_string('class Foo { void bar() { int a = true ? 1 : 2;} }')
        visitor = JavaComplexityCalculator()
        tree.accept(visitor)
        self.assertListEqual([2], visitor.mccabe_values)

    def test_visit_IfThenElse(self):
        tree = self.parser.parse_string('''
            class Foo {
                void bar() {
                    if (true) {}
                }
            }
        ''')
        visitor = JavaComplexityCalculator()
        tree.accept(visitor)
        self.assertListEqual([2], visitor.mccabe_values)

        tree = self.parser.parse_string('''
            class Foo {
                void bar() {
                    if (true) {} else ;
                }
            }
        ''')
        visitor = JavaComplexityCalculator()
        tree.accept(visitor)
        self.assertListEqual([3], visitor.mccabe_values)

    def test_visit_While(self):
        tree = self.parser.parse_string('''
            class Foo {
                void bar() {
                    while (false) {}
                }
            }
        ''')
        visitor = JavaComplexityCalculator()
        tree.accept(visitor)
        self.assertListEqual([2], visitor.mccabe_values)

if __name__ == "__main__":
    unittest.main()