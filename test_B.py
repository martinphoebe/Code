import pytest
from vendingmachine import *

pytest.main()

def test_format_coin():
    assert format_coin(2.0) == "£2"
    assert format_coin(1.0) == "£1"
    assert format_coin(0.5) == "50p"
    assert format_coin(0.2) == "20p"

def test_discount():
    assert discount(["Water"], 1.5) == 0 #no discount
    assert discount(["Water", "Soda", "Crisps"], 4.5) == 0.05 #3 items discount
    assert discount(["Chocolate", "Chocolate"], 5.0) == 0.10 #10% discount
    assert discount(["Chocolate", "Chocolate", "Chocolate"], 7.5) == 0.15 #15% discount

def test_change():
    coins, kept = change(3.5)
    assert coins == [2.0, 1.0, 0.5]
    assert kept == 0

    coins, kept = change(0.3)
    assert coins == [0.2]
    assert kept == 0.1

    coins, kept = change(5.7)
    assert coins == [2.0, 2.0, 1.0, 0.5, 0.2]
    assert kept == 0