from typing import List
import pytest
import re
from tests.utils import generate_strings_from_regex

class Assert:
    @staticmethod
    def _get_matches(regex:str)->List:
        strings = generate_strings_from_regex(regex)
        matches = [re.match(regex,string) for string in strings]
        return matches
    @staticmethod
    def assert_some_strings_match_the_regex(regex):
        matches = Assert._get_matches(regex)
        assert any(matches), f'no string matches {regex}'
    @staticmethod
    def assert_some_strings_do_not_match_the_regex(regex):
        matches = Assert._get_matches(regex)
        assert not all(matches), f'all strings match {regex}'
    @staticmethod
    def all_the_strings_match_the_regex(regex):
        matches = Assert._get_matches(regex)
        assert all(matches), f'some strings does not match {regex}'

def test_incomplete_range_1():
    regex = '^[a-g]$'
    Assert.assert_some_strings_do_not_match_the_regex(regex)
    Assert.assert_some_strings_match_the_regex(regex)


def test_incomplete_range_2():
    regex = '^[0-5]$'
    Assert.assert_some_strings_do_not_match_the_regex(regex)
    Assert.assert_some_strings_match_the_regex(regex)

def test_incomplete_range_3():
    regex = '^[A-G]$'
    Assert.assert_some_strings_do_not_match_the_regex(regex)
    Assert.assert_some_strings_match_the_regex(regex)

def test_loop_1():
    regex='^a+$'
    Assert.assert_some_strings_do_not_match_the_regex(regex)
    Assert.assert_some_strings_match_the_regex(regex)

def test_loop_2():
    regex='^a*$'
    Assert.all_the_strings_match_the_regex(regex)

def test_character_class_1():
    regex = r'^\w$'
    Assert.all_the_strings_match_the_regex(regex)

def test_character_class_2():
    regex = r'^.$'
    Assert.all_the_strings_match_the_regex(regex)

def test_character_class_3():
    regex = r"^\W$"
    Assert.assert_some_strings_match_the_regex(regex)
    Assert.assert_some_strings_do_not_match_the_regex(regex)