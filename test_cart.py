import pytest
from cart import Cart


@pytest.fixture()
def cart():
    cart = Cart(owner="Bob")
    return cart


def test_Cart_Attributes(cart):
    assert cart.owner == "Bob"
    assert cart.list == []


def test_add_item():
    cart1 = Cart(owner="Bob")
    cart1 + 'shampoo'
    assert "shampoo" in cart1.list


def test_sub_item():
    cart1 = Cart(owner="Bob")
    cart1 + ["shampoo", "grapes"]
    assert ["shampoo", "grapes"] in cart1.list

    cart1 - "shampoo"
    assert "shampoo" not in cart1.list


def test_canAddItem(cart):
    cart.addItem("bananas")
    cart.addItem("apples")
    assert cart.list == ["bananas", "apples"]


def test_cart_total():
    cart = Cart(owner="Bob")
    cart.clear_cart()
    assert cart.total == 0

    cart.update_total(60)
    assert cart.total == 60

    cart.update_total(40)
    assert cart.total == 100
