shirt_sub_categories = ['tshirt','croptop', 'polo', 'tank', 'blouse', 'cardigan', 'sweater', 'blouse', 'jacket', 'hoodie', 'jacket']
dress_sub_categories = ['gown', 'romper','jumpsuit']
pant_sub_categories = ['dresspants','jeans', 'slacks', 'sweatpants', 'shorts', 'leggings']
skirt_sub_categories = []
other = ['kimono', 'coat']

shirt_pattern = ['raglan']

# kimono?????

##################################################################################
# GROUPS: Each item can only be labelled with one label from each group
##################################################################################
categories = ['shirt', 'dress', 'pant', 'skirt']
sub_categories = shirt_sub_categories + dress_sub_categories + pant_sub_categories + skirt_sub_categories
neck = ['vneck', 'crewneck', 'scoopneck', 'sweetheartneck', 'turtleneck', 'highneck', 'offtheshoulder', 'collar', 'boatneck', 'splitneck', 'halter']
sleeve = ['longsleeve', 'shortsleeve', 'bellsleeve', 'raglansleeve', 'threequartersleeve', 'fluttersleeve', 'sleeveless']
#maybe seperate sleeve length and sleeve type?

color = ['black', 'white', 'blue', 'red', 'multicolor', 'grey', 'navy', 'red', 'pink', 'dark', 'light']
pattern = ['logo', 'floral', 'graphic', 'pattern', 'printed', 'tonal', 'embroidered', 'stripe', 'paisley', 'distressed', 'dot', 'colorblock', 'plaid', 'leopard', 'raglan']
#tribal
material = ['polyester', 'knit', 'jersey', 'lace', 'denim', 'silk', 'chiffon', 'leather', 'cotton', 'slub', 'linen', 'tweed', 'crochet', 'mesh']
texture = ['ribbed', 'pleated', 'woven']

style = ['casual', 'slit', 'highslit', 'fringehem', 'yoga']
fit = ['slim', 'relaxed', 'boxy', 'skinny','pencil', 'sheath']

pant_shape = ['boyfriend', 'skinny', 'bootcut', 'crop']

shape = ['peasant', 'muscle', 'surplice', 'peplum', 'dolman', 'kimono'] + pant_shape

length = ['mini', 'midi', 'maxi','long', 'short', 'crop'] 

#Single label groups
INVALID = ['heathered', 'ribbed', 'hood', 'lattice', 'drape', 'ruffle', 'strappy', 'racerback', 'deepv', 'panel', 'highslit']

all_labels = list(set(categories + sub_categories + neck + sleeve + color + pattern + material + texture + style + fit + pant_shape + shape + length + INVALID))

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
    'joggers':'sweatpants'
} 
skirt_replacements = {
    "body length": "maxi",
    "full length": "maxi",
    "knee length": "midi"
}
shirt_replacements = {}


