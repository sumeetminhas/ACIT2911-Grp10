class Cart:
    def __init__(self, owner):
        self.owner = owner
        self.list = []
        self.total = 0

    def addItem(self, item):
        """ adds an item to the list"""
        if item not in self.list:
            self.list.append(item)

    def __add__(self, item):
        self.list.append(item)

    def __sub__(self, item):
        if item in self.list:
            self.list.remove(item)
        # else:
        #     raise ValueError

    def clear_cart(self):
        self.list = []
        self.total = 0
    
    def update_total(self, price):
        self.total += price


if __name__ == "__main__":
    pass
