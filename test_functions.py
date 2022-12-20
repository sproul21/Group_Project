from parse_functions import *
import pytest
import math
import random
from io import StringIO
from _pytest import monkeypatch

import parse_functions

##def test_find_review():
    ##assert parse_functions.find_review('0') is True
    #assert parse_functions.find_review(1.5) is True
    #assert parse_functions.find_review(2) is True
    #assert parse_functions.find_review(2.0) is False
    #assert parse_functions.find_review(Exception) is False
    #assert parse_functions.find_review(5.0) is True

def test_find_review(monkeypatch, capfd):
    test_review = float
    simulated_input = StringIO(test_review)
    monkeypatch.setattr('sys.stdin', simulated_input)
    assert test_find_review(float) is True


