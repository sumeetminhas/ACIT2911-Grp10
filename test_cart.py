import pytest
from cart import Cart


def test_Cart_Attributes():
    cart = Cart(owner="Bob")
    assert cart.owner == "Bob"
    assert cart.list == []
