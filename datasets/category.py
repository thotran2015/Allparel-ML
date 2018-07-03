import util 
import config

class Category:

    def __init__(self, category, sub_categories, replacements):
        self.category = category
        self.sub_categories = sub_categories
        self.replacements = replacements
    
    def in_category(self, text):
        for word in text.split():
            if util.are_equal(word, self.category):
                return True
            for sub_cat in self.sub_categories:
                if util.are_equal(word, sub_cat):
                    return True
        return False

    def replace(self, tags):
        for i in range(len(tags)):
            if tags[i] in self.replacements.keys():
                tags[i] = self.replacements[tags[i]]
            elif tags[i] in config.all_replacements.keys():
                tags[i] = config.all_replacements[tags[i]]


