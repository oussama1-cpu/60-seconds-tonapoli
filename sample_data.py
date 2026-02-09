"""
Sample data script for 60 Seconds to Napoli
Run this script to populate the database with real menu data

Usage:
    python manage.py shell < sample_data.py
    
Or in Django shell:
    python manage.py shell
    >>> exec(open('sample_data.py').read())
"""

from menu.models import (
    Category, MenuItem, Ingredient, MenuItemIngredient,
    Customization, RestaurantInfo
)
from decimal import Decimal

print("Creating 60 Seconds to Napoli menu data...")
print("=" * 50)

# Create Restaurant Info
print("\n1. Creating Restaurant Information...")
restaurant_info, created = RestaurantInfo.objects.get_or_create(
    id=1,
    defaults={
        'name': '60 Seconds to Napoli',
        'description': 'Award winning Neapolitan pizza. Original pizza baked at 485°C for 60 seconds with dough that rests up to 72 hours.',
        'phone': '',
        'email': 'info@60secondstonapoli.de',
        'address': 'Rüttenscheider Str. 199, 45131 Essen, Germany',
        'opening_hours': 'Monday-Sunday: 11:30-22:00',
        'currency_symbol': '€',
        'tax_rate': Decimal('19.00'),
    }
)
if created:
    print("   ✓ Restaurant info created")
else:
    print("   ℹ Restaurant info already exists")

# Create Categories
print("\n2. Creating Categories...")
categories_data = [
    {'name': 'Antipasti', 'description': 'Starters and salads', 'order': 1},
    {'name': 'Classic Pizzas', 'description': 'Traditional Neapolitan pizzas baked at 485°C for 60 seconds', 'order': 2},
    {'name': 'Premium Pizzas', 'description': 'Signature pizzas with premium ingredients', 'order': 3},
    {'name': 'Specials', 'description': 'Seasonal and special pizzas', 'order': 4},
    {'name': 'Vegan', 'description': 'Vegan pizza options', 'order': 5},
    {'name': 'Desserts', 'description': 'Sweet endings - Dolci', 'order': 6},
    {'name': 'Drinks', 'description': 'Beverages, wines and cocktails', 'order': 7},
]

categories = {}
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    categories[cat_data['name']] = category
    if created:
        print(f"   ✓ Created category: {cat_data['name']}")
    else:
        print(f"   ℹ Category exists: {cat_data['name']}")

# Create Ingredients
print("\n3. Creating Ingredients...")
ingredients_data = [
    {'name': 'San Marzano Tomatensoße DOP', 'is_allergen': False},
    {'name': 'Fior di Latte', 'is_allergen': True},
    {'name': 'Burrata', 'is_allergen': True},
    {'name': 'Parmigiano Reggiano 24 Monate DOP', 'is_allergen': True},
    {'name': 'Provolone DOP', 'is_allergen': True},
    {'name': 'Frisches Basilikum', 'is_allergen': False},
    {'name': 'Kaltgepresstes Olivenöl', 'is_allergen': False},
    {'name': 'Knoblauch', 'is_allergen': False},
    {'name': 'Rucola', 'is_allergen': False},
    {'name': 'Kirschtomaten', 'is_allergen': False},
    {'name': 'Parmaschinken 24 Monate DOP', 'is_allergen': False},
    {'name': 'Salami Napoli', 'is_allergen': False},
    {'name': 'Mangalitza Bacon', 'is_allergen': False},
    {'name': 'Chorizo de Bellota', 'is_allergen': False},
    {'name': 'Bresaola Black Angus', 'is_allergen': False},
    {'name': 'Argentinische Riesengarnelen', 'is_allergen': True},
    {'name': 'Thunfisch', 'is_allergen': True},
    {'name': 'Hummerfleisch', 'is_allergen': True},
    {'name': 'Champignons', 'is_allergen': False},
    {'name': 'Spinat', 'is_allergen': False},
    {'name': 'Zucchini', 'is_allergen': False},
    {'name': 'Brokkoli', 'is_allergen': False},
    {'name': 'Rote Zwiebeln', 'is_allergen': False},
    {'name': 'Bio Chili-Honig', 'is_allergen': False},
    {'name': 'Schwarzer Trüffel', 'is_allergen': False},
    {'name': 'Vanozza (Vegan Mozzarella)', 'is_allergen': False},
]

ingredients = {}
for ing_data in ingredients_data:
    ingredient, created = Ingredient.objects.get_or_create(
        name=ing_data['name'],
        defaults=ing_data
    )
    ingredients[ing_data['name']] = ingredient
    if created:
        print(f"   ✓ Created ingredient: {ing_data['name']}")

# Create Menu Items
print("\n4. Creating Menu Items...")

# Antipasti
antipasti = [
    {
        'name': 'Mixed Antipasti',
        'description': 'Parmaschinken 24 Monate DOP, Salami Napoli, Mangalitza Bacon, Büffelmozzarella DOP, Parmigiano Reggiano 24 Monate DOP, Bresaola vom Black Angus Rind, Chorizo de Bellota, Kalamata-Oliven, Bread',
        'price': Decimal('16.00'),
        'preparation_time': 10,
    },
    {
        'name': 'Cheese Roll',
        'description': 'Provolone DOP, steirischer Bergkäse, Trüffelmayonnaise',
        'price': Decimal('9.00'),
        'is_vegetarian': True,
        'preparation_time': 8,
    },
    {
        'name': 'Grünzeug',
        'description': 'Wildkräutersalat, Kirschtomaten, rote Zwiebeln, Kalamata-Oliven, Gurke, Bread, Balsamico Dressing',
        'price': Decimal('10.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 5,
    },
    {
        'name': 'Caesar Salad',
        'description': 'Romanasalat, Kirschtomaten, Parmigiano Reggiano 24 Monate DOP, hausgemachtes Caesar Dressing, Kikok-Hähnchenfilet, Bread',
        'price': Decimal('14.00'),
        'preparation_time': 8,
    },
]

for item_data in antipasti:
    item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        category=categories['Antipasti'],
        defaults={**item_data, 'is_available': True}
    )
    if created:
        print(f"   ✓ Created: {item_data['name']}")

# Classic Pizzas
classic_pizzas = [
    {
        'name': 'Marinara',
        'description': 'San Marzano Tomatensoße DOP, Knoblauch, Oregano',
        'price': Decimal('10.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 1,
    },
    {
        'name': 'Margherita',
        'description': 'San Marzano Tomatensoße DOP, Fior di Latte, frisches Basilikum, kaltgepresstes Olivenöl',
        'price': Decimal('13.00'),
        'is_vegetarian': True,
        'is_featured': True,
        'preparation_time': 1,
    },
    {
        'name': 'Cowabunga',
        'description': 'San Marzano Tomatensoße DOP, Salami Napoli, Fior di Latte',
        'price': Decimal('14.00'),
        'preparation_time': 1,
    },
    {
        'name': 'Schinken Champignons',
        'description': 'San Marzano Tomatensoße DOP, Fior di Latte, Mangalitza Schinken, Champignons',
        'price': Decimal('14.00'),
        'preparation_time': 1,
    },
    {
        'name': 'Green Mamba',
        'description': 'San Marzano Tomatensoße DOP, Fior di Latte, Rucola, Zucchini, Brokkoli, kaltgepresstes Olivenöl',
        'price': Decimal('14.00'),
        'is_vegetarian': True,
        'preparation_time': 1,
    },
    {
        'name': 'Arnie',
        'description': 'Steirischer Bergkäse, Fior di Latte, Babyspinat, Knoblauch, schwarzer Pfeffer',
        'price': Decimal('14.00'),
        'is_vegetarian': True,
        'preparation_time': 1,
    },
    {
        'name': 'White Tuna',
        'description': 'San Marzano Tomatensoße DOP, Fior di Latte, Thunfisch, rote Zwiebeln',
        'price': Decimal('15.00'),
        'preparation_time': 1,
    },
]

for item_data in classic_pizzas:
    item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        category=categories['Classic Pizzas'],
        defaults={**item_data, 'is_available': True}
    )
    if created:
        print(f"   ✓ Created: {item_data['name']}")

# Premium Pizzas
premium_pizzas = [
    {
        'name': 'The Rock',
        'description': 'Burrata, hausgemachtes frisches Basilikum-Pesto, Parmigiano Reggiano 24 Monate DOP, Kirschtomaten, Pinienkerne',
        'price': Decimal('16.00'),
        'is_vegetarian': True,
        'is_featured': True,
        'preparation_time': 1,
    },
    {
        'name': 'Salsiccia Style',
        'description': 'Provolone DOP, Fior di Latte, Fenchel-Salsiccia, Kirschtomaten, Basilikum, schwarzer Pfeffer',
        'price': Decimal('15.00'),
        'preparation_time': 1,
    },
    {
        'name': 'Don Diablo',
        'description': 'San Marzano Tomatensoße DOP, Chorizo de Bellota, Fior di Latte, Bio Chili-Honig, geräuchertes Paprikapulver',
        'price': Decimal('15.00'),
        'spice_level': 'medium',
        'is_featured': True,
        'preparation_time': 1,
    },
    {
        'name': 'The Beast',
        'description': 'San Marzano Tomatensoße DOP, Bresaola vom Black Angus Rind, Parmigiano Reggiano 24 Monate DOP, Kirschtomaten, Fior di Latte, Olivenöl',
        'price': Decimal('16.00'),
        'preparation_time': 1,
    },
    {
        'name': 'Bacon N Cheese',
        'description': 'Provolone DOP, Mangalitza Bacon, Fior di Latte, Champignons, rote Zwiebeln, schwarzer Pfeffer',
        'price': Decimal('15.00'),
        'preparation_time': 1,
    },
    {
        'name': 'Burrata Bomb',
        'description': 'San Marzano Tomatensoße DOP, Burrata, Crispy Nduja, spicy Gremolata, Parmigiano Reggiano 24 Monate DOP, Kirschtomaten, Chiliöl',
        'price': Decimal('17.00'),
        'spice_level': 'hot',
        'is_featured': True,
        'preparation_time': 1,
    },
    {
        'name': 'Parma 24',
        'description': 'San Marzano Tomatensoße DOP, Fior di Latte, Rucola, Olivenöl, Parmaschinken 24 Monate DOP, Parmigiano Reggiano 24 Monate DOP',
        'price': Decimal('17.00'),
        'is_featured': True,
        'preparation_time': 1,
    },
    {
        'name': 'Gamba',
        'description': 'San Marzano Tomatensoße DOP, argentinische Riesengarnelen, Fior di Latte, Spinat, Knoblauchöl',
        'price': Decimal('18.00'),
        'preparation_time': 1,
    },
    {
        'name': 'Oh My Truffle',
        'description': 'Weiße Trüffelcream, Fior di Latte, schwarzer Trüffel, Parmigiano Reggiano 24 Monate DOP',
        'price': Decimal('19.00'),
        'is_vegetarian': True,
        'is_featured': True,
        'preparation_time': 1,
    },
]

for item_data in premium_pizzas:
    item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        category=categories['Premium Pizzas'],
        defaults={**item_data, 'is_available': True}
    )
    if created:
        print(f"   ✓ Created: {item_data['name']}")

# Specials
specials = [
    {
        'name': 'The Royal Lobster',
        'description': 'San Marzano Tomatensoße DOP, Cream, Fior di Latte, Hummerfleisch, französische gesalzene Butter, Frühlingszwiebeln, Sriracha-Mayonnaise',
        'price': Decimal('30.00'),
        'is_featured': True,
        'preparation_time': 1,
    },
    {
        'name': 'Züri Raclette Royal',
        'description': 'Smashed Rösti, Parmaschinken 24 Monate DOP, Gewürzgurken, Schnittlauch, Raclettekäse, kaltgepresstes Olivenöl, schwarzer Pfeffer',
        'price': Decimal('18.00'),
        'preparation_time': 1,
    },
    {
        'name': 'American Steak Pizza',
        'description': 'San Marzano Tomatensoße DOP, Fior di Latte, Rucola, konfierte Kirschtomaten, amerikanisches Rumpsteak, Parmigiano Reggiano 24 Monate DOP, frittierter Knoblauch, hausgemachte Kräuterbutter, Meersalzflocken',
        'price': Decimal('22.00'),
        'is_featured': True,
        'preparation_time': 1,
    },
    {
        'name': 'Vodka Pepperhoney',
        'description': '9 Mile-Vodkatomatensoße, Fior di Latte, Provolone DOP, Pepperonisalami, Oregano, Bio-Chilihonig, Parmesanschnee',
        'price': Decimal('16.00'),
        'spice_level': 'medium',
        'preparation_time': 1,
    },
    {
        'name': 'Hoppy Heaven',
        'description': 'Gelbe Tomatensauce, geräucherter Fior di Latte, braune Champignons, Porchetta, Rosmarin, Chili, Pfeffer',
        'price': Decimal('18.00'),
        'preparation_time': 1,
    },
    {
        'name': 'Trufflepasta in a Pizza Bowl',
        'description': 'Weiße Trüffelcream, Bucatini, Parmigiano Reggiano 24 Monate DOP, schwarzer Trüffel, Basilikum, schwarzer Pfeffer',
        'price': Decimal('19.00'),
        'is_vegetarian': True,
        'is_featured': True,
        'preparation_time': 1,
    },
]

for item_data in specials:
    item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        category=categories['Specials'],
        defaults={**item_data, 'is_available': True}
    )
    if created:
        print(f"   ✓ Created: {item_data['name']}")

# Vegan Pizzas
vegan_pizzas = [
    {
        'name': 'Margherita Vegan',
        'description': 'San Marzano Tomatensoße DOP, Vanozza, frisches Basilikum, kaltgepresstes Olivenöl',
        'price': Decimal('14.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 1,
    },
    {
        'name': 'Vegan Salami',
        'description': 'San Marzano Tomatensoße DOP, Sim Sala Mi, Vanozza, frisches Basilikum, Olivenöl',
        'price': Decimal('15.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 1,
    },
    {
        'name': 'Vegan Beef Chimichurri',
        'description': 'San Marzano Tomatensoße DOP, Vanozza, planted.steak, Rucola, Chimichurri, schwarzer Pfeffer, frisches Basilikum',
        'price': Decimal('17.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'is_featured': True,
        'preparation_time': 1,
    },
]

for item_data in vegan_pizzas:
    item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        category=categories['Vegan'],
        defaults={**item_data, 'is_available': True}
    )
    if created:
        print(f"   ✓ Created: {item_data['name']}")

# Desserts
desserts = [
    {
        'name': 'Hausgemachtes Schokotörtchen',
        'description': 'Hausgemachtes Schokotörtchen mit flüssigem Kern, wahlweise mit Vanille Eis',
        'price': Decimal('8.00'),
        'is_vegetarian': True,
        'is_featured': True,
        'preparation_time': 5,
    },
    {
        'name': 'Wintertiramisu',
        'description': 'Mascarponecreme, Lotuscream, Lotuscrumble',
        'price': Decimal('8.00'),
        'is_vegetarian': True,
        'preparation_time': 5,
    },
    {
        'name': 'Baskischer Käsekuchen',
        'description': 'Hausgemachter baskischer Käsekuchen, wahlweise mit Lotuscream',
        'price': Decimal('7.00'),
        'is_vegetarian': True,
        'preparation_time': 5,
    },
    {
        'name': 'Vegan Strawberry Crumble',
        'description': 'Erdbeeren, vegane Vanillecream, veganer Kekscrumble',
        'price': Decimal('7.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 5,
    },
    {
        'name': 'Espresso Affogato',
        'description': 'Vanille Eis, Espressocrumble, Espresso',
        'price': Decimal('6.00'),
        'is_vegetarian': True,
        'preparation_time': 3,
    },
    {
        'name': 'Pastel de Nata Pizza',
        'description': 'Süße Pizza im Pastel de Nata Stil',
        'price': Decimal('9.00'),
        'is_vegetarian': True,
        'is_featured': True,
        'preparation_time': 5,
    },
    {
        'name': 'Dubai Schokoladen Pizza',
        'description': 'Kikis Dubai Schokoladen Pizza - Special',
        'price': Decimal('12.00'),
        'is_vegetarian': True,
        'is_featured': True,
        'preparation_time': 5,
    },
]

for item_data in desserts:
    item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        category=categories['Desserts'],
        defaults={**item_data, 'is_available': True}
    )
    if created:
        print(f"   ✓ Created: {item_data['name']}")

# Drinks
drinks = [
    {
        'name': 'Espresso Macchiato',
        'description': 'Espresso with a dash of milk foam',
        'price': Decimal('3.00'),
        'is_vegetarian': True,
        'preparation_time': 3,
    },
    {
        'name': 'Iced Coffee Latte',
        'description': 'Cold coffee with milk',
        'price': Decimal('4.50'),
        'is_vegetarian': True,
        'preparation_time': 3,
    },
    {
        'name': 'Bitburger Pils',
        'description': 'German Pilsner 0.3L',
        'price': Decimal('4.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 1,
    },
    {
        'name': 'Benediktiner Weizen',
        'description': 'German wheat beer 0.5L',
        'price': Decimal('5.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 1,
    },
    {
        'name': 'Sarti Spritz',
        'description': 'Italian aperitif cocktail',
        'price': Decimal('9.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 3,
    },
    {
        'name': 'Gin Tonic',
        'description': 'Classic gin and tonic',
        'price': Decimal('10.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 3,
    },
    {
        'name': 'Espresso Martini',
        'description': 'Vodka, coffee liqueur, espresso',
        'price': Decimal('12.00'),
        'is_vegetarian': True,
        'preparation_time': 5,
    },
    {
        'name': 'Riesling Good Vibes 2023',
        'description': 'German white wine - glass',
        'price': Decimal('7.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 1,
    },
    {
        'name': 'Aix Rosé 2023',
        'description': 'Grenache, Cinsault, Syrah - glass',
        'price': Decimal('8.00'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 1,
    },
    {
        'name': 'Coca-Cola Zero',
        'description': 'Sugar-free cola 0.33L',
        'price': Decimal('3.50'),
        'is_vegetarian': True,
        'is_vegan': True,
        'preparation_time': 1,
    },
]

for item_data in drinks:
    item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        category=categories['Drinks'],
        defaults={**item_data, 'is_available': True}
    )
    if created:
        print(f"   ✓ Created: {item_data['name']}")

# Create Customizations
print("\n5. Creating Customizations...")
customizations_data = [
    {'name': 'Small (8")', 'customization_type': 'size', 'price_modifier': Decimal('-2.00')},
    {'name': 'Large (14")', 'customization_type': 'size', 'price_modifier': Decimal('3.00')},
    {'name': 'Extra Large (16")', 'customization_type': 'size', 'price_modifier': Decimal('5.00')},
    {'name': 'Extra Cheese', 'customization_type': 'extra', 'price_modifier': Decimal('2.00')},
    {'name': 'Extra Toppings', 'customization_type': 'extra', 'price_modifier': Decimal('1.50')},
    {'name': 'Gluten-Free Crust', 'customization_type': 'other', 'price_modifier': Decimal('3.00')},
    {'name': 'Side Salad', 'customization_type': 'side', 'price_modifier': Decimal('4.00')},
    {'name': 'French Fries', 'customization_type': 'side', 'price_modifier': Decimal('3.50')},
    {'name': 'Garlic Sauce', 'customization_type': 'sauce', 'price_modifier': Decimal('0.50')},
    {'name': 'Spicy Sauce', 'customization_type': 'sauce', 'price_modifier': Decimal('0.50')},
]

for custom_data in customizations_data:
    customization, created = Customization.objects.get_or_create(
        name=custom_data['name'],
        defaults=custom_data
    )
    if created:
        print(f"   ✓ Created customization: {custom_data['name']}")

print("\n" + "=" * 50)
print("✅ Sample data creation completed!")
print("\nSummary:")
print(f"   Categories: {Category.objects.count()}")
print(f"   Menu Items: {MenuItem.objects.count()}")
print(f"   Ingredients: {Ingredient.objects.count()}")
print(f"   Customizations: {Customization.objects.count()}")
print("\nYou can now:")
print("   1. Access admin at: http://127.0.0.1:8000/admin/")
print("   2. View API at: http://127.0.0.1:8000/api/")
print("   3. Check docs at: http://127.0.0.1:8000/swagger/")
print("=" * 50)
