import category

shirt_sub_categories = ['tshirt','croptop', 'polo', 'tank', 'blouse', 'cardigan', 'sweater', 'blouse', 'jacket', 'hoodie', 'jacket', "top"]
dress_sub_categories = ['gown', 'romper','jumpsuit']
pant_sub_categories = ['dresspants','jeans', 'slacks', 'sweatpants', 'shorts', 'leggings']
skirt_sub_categories = []
other = ['kimono', 'coat']

shirt_pattern = ['raglan']

# Define replacements (i.e. synonyms) - some are defined per category
all_replacements = {
    'tee':'tshirt',
    "neckline":"neck", 
    "sleeved":"sleeve", 
    "sleeves":"sleeve", 
    'hooded':'hood', 
    'ruffled':'ruffle',
    "cuff":"cuffs", 
    "nosleeve": "sleeveless",
    "pants": "pant",
    "roundneck":"crewneck",
    'draped':'drape',
    "uneck":"crewneck", 
    "fringedhem":"fringehem", 
    "longline":"long", 
    "cropped":"crop"
}
dress_replacements = {
    "body length": "maxi",
    "full length": "maxi",
    "knee length": "midi"
}
pant_replacements = {
    'sweats': 'sweatpants', 
    'joggers':'sweatpants', 
    'bootcut': 'flare'
} 
skirt_replacements = {
    "body length": "maxi",
    "full length": "maxi",
    "knee length": "midi"
}
shirt_replacements = {}

dress = category.Category(
        category = 'dress',
        sub_categories = dress_sub_categories, 
        replacements = dress_replacements)
shirt = category.Category(
        category = 'shirt', 
        sub_categories = shirt_sub_categories, 
        replacements = shirt_replacements)
pant =  category.Category(
        category = 'pant',   
        sub_categories = pant_sub_categories,  
        replacements = pant_replacements)
skirt = category.Category(
        category = 'skirt', 
        sub_categories = skirt_sub_categories, 
        replacements = skirt_replacements)

##################################################################################
# GROUPS: Each item can only be labelled with one label from each group
##################################################################################
class Group:
    def __init__(self, name, labels, categories):
        self.labels = labels
        self.categories = categories

neck = Group(
            name = "neck", 
            labels = [
                'vneck', 
                'crewneck', 
                'scoopneck', 
                'sweetheartneck', 
                'turtleneck', 
                'highneck', 
                'offtheshoulder', 
                'collar', 
                'boatneck', 
                'splitneck', 
                'halter', 
                'oneshoulder', 
                'straightneck'
            ], 
            categories = [dress, shirt]
        )

sleeve_shape = Group(
            name= "sleeve_shape", 
            labels = [
                'bellsleeve', 
                'raglansleeve', 
                'fluttersleeve', 
            ], 
            categories = [dress, shirt]
        )

sleeve_length = Group(
            name= "sleeve_length", 
            labels = [
                'longsleeve', 
                'shortsleeve', 
                'threequartersleeve', 
                'sleeveless', 
                'strapless'
            ], 
            categories = [dress, shirt]
        )

color = Group(
            name = "color", 
            labels = [
                'black', 
                'white', 
                'blue', 
                'red', 
                'multicolor', 
                'grey', 
                'navy', 
                'red', 
                'pink', 
                'dark', 
                'light'
            ], 
            categories = [dress, shirt, pant, skirt]
        )

pattern = Group(
            name = "pattern", 
            labels = [
                'logo', 
                'floral', 
                'graphic', 
                'pattern', 
                'printed', 
                'tonal', 
                'embroidered', 
                'stripe', 
                'paisley', 
                'distressed', 
                'dot', 
                'colorblock', 
                'plaid', 
                'leopard', 
                'tribal'
            ], 
            categories = [dress, shirt, pant, skirt]
        )
material = Group(
                name = "material", 
                labels = [
                    'polyester', 
                    'knit', 
                    'jersey', 
                    'lace', 
                    'denim', 
                    'silk', 
                    'chiffon', 
                    'leather', 
                    'cotton', 
                    'slub', 
                    'linen', 
                    'tweed', 
                    'crochet', 
                    'mesh'
                ], 
                categories = [dress, shirt, pant, skirt]
            )

texture = Group(
            name = "texture", 
            labels = [
                'ribbed', 
                'pleated', 
                'woven'
            ], 
            categories = [dress, shirt, pant, skirt]
        )

style = Group(
            name = "style", 
            labels = [
                'casual', 
                'slit', 
                'highslit', 
                'fringehem', 
                'yoga'
            ], 
            categories = [dress, shirt, pant, skirt])

fit = Group(
        name = "fit", 
        labels = [
            'slim', 
            'relaxed', 
            'boxy', 
            'skinny',
            'pencil', 
            'sheath'
        ], 
        categories = [dress, shirt, pant, skirt])

pant_shape = Group(
                name = "pant_shape", 
                labels = [
                    'boyfriend', 
                    'skinny', 
                    'flare', 
                    'crop'
                ], 
                categories = [pant]
            )

shape = Group(
            name = 'shape', 
            labels = [
                'peasant', 
                'muscle', 
                'surplice', 
                'peplum', 
                'dolman', 
                'kimono'
            ], 
            categories = [dress, shirt, skirt])

length = Group(
            name="skirt_length", 
            labels = ['mini', 'midi', 'maxi'] ,
            categories = [dress, shirt]
        )

invalid = Group(
            name = "invalid", 
            labels = ['heathered', 'ribbed', 'hood', 'lattice', 'drape', 'ruffle', 'strappy', 'racerback', 'deepv', 'panel', 'highslit'], 
            categories = [dress, skirt, pant, skirt])

