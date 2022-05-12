class Cart:
    def __init__(self, owner):
        self.owner = owner
        self.list = []

    def __add__(self, item):
        self.list.append(item)
    
    def __sub__(self, item):
        if item in self.list: self.list.remove(item)
        else: print('Item not in the cart')

    def clear_cart(self):
        self.list = []

if __name__ == "__main__":
    pass