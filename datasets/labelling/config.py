shirt_sub_categories = ['tshirt','croptop', 'polo', 'tank', 'blouse']
dress_sub_categories = ['gown']
pant_sub_categories = ['jeans', 'slacks', 'sweatpants']
skirt_sub_categories = []
# RULE: CAN ONLY HAVE ONE LABEL FROM EACH
categories = ['shirt', 'dress', 'pant', 'skirt']
sub_categories = shirt_sub_categories + dress_sub_categories + pant_sub_categories + skirt_sub_categories
neck = ['vneck', 'crewneck', 'scoopneck', 'sweetheartneck', 'turtleneck', 'highneck', 'roundneck', 'offtheshoulder', 'collar']
#sleeve = ['longsleeve', 'shortsleeve', 'bellsleeve', 'raglansleeve', 'threequartersleeve', 'fluttersleeve', 'insleeve', 'nosleeve']
#color = ['black', 'white', 'blue', 'red', 'multicolor', 'grey', 'navy', 'red', 'pink', 'dark']
#pattern = ['logo', 'floral', 'graphic', 'pattern', 'printed', 'tonal', 'embroidered', 'ruffled', 'stripe']
#fit = ['slim', 'relaxed']
# material - could do but not sure how you get that from images
material = ['polyester', 'knit', 'jersey', 'lace', 'ribbed', 'woven', 'denim', 'silk']
style = ['casual', 'straps', 'slit']
length = ['mini', 'midi', 'maxi', 'long', 'short']
labels = neck #categories + sub_categories + neck + sleeve + color + pattern + fit + material + style + length
groups = [neck] #[categories, sub_categories, neck#, sleeve, color, pattern, fit, material, style, length]
group_names = ['neck']

all_replacements = {
    "neckline":"neck", 
    "sleeved":"sleeve", 
    "sleeves":"sleeve", 
    "cuff":"cuffs", 
    "nosleeve": "sleeveless",
    "pants": "pant",
}
dress_replacements = {
    "body length": "maxi",
    "full length": "maxi",
    "knee length": "midi"
}
pant_replacements = {
    'sweats': 'sweatpants'
} 
skirt_replacements = {
    "body length": "maxi",
    "full length": "maxi",
    "knee length": "midi"
}
shirt_replacements = {}


