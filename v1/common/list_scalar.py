#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from graphene import Scalar
from graphql.language import ast


class List(Scalar):
    """
    The `List` scalar type represents a python list.
    """

    parse_value = list
    serialize = list

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.ListValue):
            return [item.value for item in node.values]
