class Cart:
    def __init__(self, owner):
        self.owner = owner
        self.list = []

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


if __name__ == "__main__":
    pass
