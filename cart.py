class Cart:
    def __init__(self, owner):
        self.owner = owner
        self.list = []

    def __add__(self, item):
        self.list.append(item)
    
    def __sub__(self, item):
        if item in self.list: self.list.remove(item)
        else: print('Item not in the cart')

    def add_item(self, item):
        self.list.append(item)

if __name__ == "__main__":
    pass