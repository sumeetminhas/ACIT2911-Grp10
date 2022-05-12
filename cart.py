class Cart:
    def __init__(self, owner):
        self.owner = owner
        self.list = []
        self.total = 0

    def __add__(self, item):
        self.list.append(item)
    
    def __sub__(self, item):
        if item in self.list: self.list.remove(item)
        else: print('Item not in the cart')

    def clear_cart(self):
        self.list = []
        self.total = 0
    
    def update_total(self, price):
        self.total += price

if __name__ == "__main__":
    pass