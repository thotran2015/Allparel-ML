
class Group:

    def __init__(self, name, labels, categories):
        self.name = name
        self.labels = labels
        self.categories = categories

    def has_category(self, category):
        for cat in self.categories:
            return True
        return False


