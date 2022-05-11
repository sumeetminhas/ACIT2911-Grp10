import pytest
from cart import Cart


@pytest.fixture()
def cart():
    cart = Cart(owner="Bob")
    return cart


def test_Cart_Attributes(cart):
    assert cart.owner == "Bob"
    assert cart.list == []


def test_canAddItem(cart):
    cart.addItem("bananas")
