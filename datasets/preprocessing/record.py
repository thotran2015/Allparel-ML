 
class Record:
    def __init__(self, image_filename, title, description, product_url, raw_category, category, pos, neg, allparel_tags=[], predicted_confidences=[]):
        self.image_filename = image_filename
        self.description = description
        self.title = title
        self.product_url = product_url
        #self.image_url = image_url
        #self.brand = brand
        self.raw_category = raw_category

        #computed 
        self.category =  category
        self.positive_tags= pos
        self.negative_tags = neg

        self.allparel_tags = allparel_tags
        self.predicted_confidences = predicted_confidences



    def __hash__(self):
        return hash(self.image_filename)

    def __eq__(self, other):
        return self.image_filename == other.image_filename

    def dict(self):
        d = vars(self)
        d['category'] = self.category.category
        return d



