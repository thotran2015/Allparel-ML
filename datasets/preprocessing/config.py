import category
import group

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
    "cropped":"crop", 
    "highslit":"slit"
}
dress_replacements = {
    "bodylength": "maxi",
    "fulllength": "maxi",
    "kneelength": "midi"
}
pant_replacements = {
    'sweats': 'sweatpants', 
    'joggers':'sweatpants', 
    'bootcut': 'flare'
} 
skirt_replacements = {
    "bodylength": "maxi",
    "fulllength": "maxi",
    "kneelength": "midi"
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
neck = group.Group(
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
                'straightneck', 
                'other'
            ], 
            categories = [dress, shirt]
        )

sleeve_shape = group.Group(
            name= "sleeve_shape", 
            labels = [
                'bellsleeve', 
                'raglansleeve', 
                'fluttersleeve', 
            ], 
            categories = [dress, shirt]
        )

sleeve_length = group.Group(
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

color = group.Group(
            name = "color", 
            labels = [
                'black', 
                'white', 
                'beige',
                'blue', 
                'red', 
                'blue',
                'yellow',
                'grey', 
                'navy', 
                'red', 
                'pink', 
                'green',
                'orange',
                'purple',
                'brown',
                'gold',
                'silver',
                'multicolor', 

            ], 
            categories = [dress, shirt, pant, skirt]
        )

pattern = group.Group(
            name = "pattern", 
            labels = [
                'logo', 
                'floral', 
                'graphic', 
                #'pattern', 
                #'printed', 
                #'tonal', 
                'embroidered', 
                'stripe', 
                'paisley', 
                'distressed', 
                'dot', 
                'colorblock', 
                'plaid', 
                'leopard'
                #'tribal'
            ], 
            categories = [dress, shirt, pant, skirt]
        )
material = group.Group(
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

texture = group.Group(
            name = "texture", 
            labels = [
                'ribbed', 
                'pleated', 
                'woven',
                'drape',
                'ruffle'
            ], 
            categories = [dress, shirt, pant, skirt]
        )

style = group.Group(
            name = "style", 
            labels = [
                'casual', 
                'slit', 
                'highslit', 
                'fringehem', 
                'yoga'
            ], 
            categories = [dress, shirt, pant, skirt])

fit = group.Group(
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

pant_shape = group.Group(
                name = "pant_shape", 
                labels = [
                    'boyfriend', 
                    'skinny', 
                    'flare', 
                    'straight',
                    'crop'
                ], 
                categories = [pant]
            )

shape = group.Group(
            name = 'shape', 
            labels = [
                'peasant', 
                'muscle', 
                'surplice', 
                'peplum', 
                'dolman', 
                'kimono', 
            ], 
            categories = [dress, shirt, skirt])

length = group.Group(
            name="skirt_length", 
            labels = ['mini', 'midi', 'maxi'] ,
            categories = [dress, shirt]
        )

invalid = group.Group(
            name = "invalid", 
            labels = ['heathered', 'hood', 'lattice' , 'strappy', 'racerback', 'deepv', 'panel', 'highslit'], 
            categories = [dress, skirt, pant, skirt])

