"""
Script pour peupler la base de données avec le vrai menu de 60 Seconds to Napoli
Avec de belles photos depuis Unsplash
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_api.settings')
django.setup()

from menu.models import Category, MenuItem

# Supprimer les anciennes données de test
print("🗑️  Suppression des anciennes données...")
MenuItem.objects.all().delete()

# Créer les catégories si elles n'existent pas
print("📁 Création des catégories...")
appetizers, _ = Category.objects.get_or_create(
    name="Appetizers",
    defaults={'description': 'Starters and Antipasti', 'order': 1, 'is_active': True}
)
pizza, _ = Category.objects.get_or_create(
    name="Pizza",
    defaults={'description': 'Neapolitan Style Pizza', 'order': 2, 'is_active': True}
)
pasta, _ = Category.objects.get_or_create(
    name="Pasta",
    defaults={'description': 'Fresh Italian Pasta', 'order': 3, 'is_active': True}
)
salads, _ = Category.objects.get_or_create(
    name="Salads",
    defaults={'description': 'Fresh Salads', 'order': 4, 'is_active': True}
)
desserts, _ = Category.objects.get_or_create(
    name="Desserts",
    defaults={'description': 'Sweet Endings', 'order': 5, 'is_active': True}
)
beverages, _ = Category.objects.get_or_create(
    name="Beverages",
    defaults={'description': 'Drinks and Coffee', 'order': 6, 'is_active': True}
)
print("✅ Catégories créées!")

print("📋 Création du menu réel...")

# ==================== STARTERS / ANTIPASTI ====================
starters = [
    {
        'name': 'Tomato Bruschetta',
        'description': 'Grilled bread topped with fresh tomatoes, garlic, basil and olive oil',
        'price': 6.50,
        'image': 'https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?w=800',
        'category': appetizers,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
    {
        'name': 'Caprese Salad',
        'description': 'Fresh mozzarella, tomatoes, basil, olive oil, balsamic glaze',
        'price': 8.90,
        'image': 'https://images.unsplash.com/photo-1608897013039-887f21d8c804?w=800',
        'category': appetizers,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
    {
        'name': 'Carpaccio',
        'description': 'Thinly sliced beef with arugula, parmesan and lemon',
        'price': 12.50,
        'image': 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=800',
        'category': appetizers,
        'spice_level': 'none',
    },
    {
        'name': 'Garlic Bread',
        'description': 'Toasted bread with garlic butter and herbs',
        'price': 4.90,
        'image': 'https://images.unsplash.com/photo-1573140401552-388e3496f4de?w=800',
        'category': appetizers,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
    {
        'name': 'Antipasti Misti',
        'description': 'Selection of Italian cold cuts, cheeses and olives',
        'price': 14.90,
        'image': 'https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=800',
        'category': appetizers,
        'spice_level': 'none',
    },
]

for item_data in starters:
    MenuItem.objects.create(**item_data)
    print(f"  ✅ {item_data['name']}")

# ==================== PIZZAS ====================
pizzas = [
    {
        'name': 'Margherita',
        'description': 'Tomato sauce, mozzarella, basil, olive oil',
        'price': 10.90,
        'image': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800',
        'category': pizza,
        'is_vegetarian': True,
        'is_featured': True,
        'spice_level': 'none',
    },
    {
        'name': 'Diavola',
        'description': 'Tomato sauce, mozzarella, spicy salami, chili',
        'price': 13.90,
        'image': 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=800',
        'category': pizza,
        'spice_level': 'hot',
    },
    {
        'name': 'Quattro Stagioni',
        'description': 'Tomato sauce, mozzarella, ham, mushrooms, artichokes, olives',
        'price': 14.90,
        'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800',
        'category': pizza,
        'spice_level': 'none',
    },
    {
        'name': 'Capricciosa',
        'description': 'Tomato sauce, mozzarella, ham, mushrooms, artichokes',
        'price': 13.90,
        'image': 'https://images.unsplash.com/photo-1571407970349-bc81e7e96f47?w=800',
        'category': pizza,
        'spice_level': 'none',
    },
    {
        'name': 'Vegetariana',
        'description': 'Tomato sauce, mozzarella, grilled vegetables, olives',
        'price': 12.90,
        'image': 'https://images.unsplash.com/photo-1511689660979-10d2b1aada49?w=800',
        'category': pizza,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
    {
        'name': 'Tonno',
        'description': 'Tomato sauce, mozzarella, tuna, onions, olives',
        'price': 13.50,
        'image': 'https://images.unsplash.com/photo-1595854341625-f33ee10dbf94?w=800',
        'category': pizza,
        'spice_level': 'none',
    },
    {
        'name': 'Quattro Formaggi',
        'description': 'Mozzarella, gorgonzola, parmesan, fontina cheese',
        'price': 13.90,
        'image': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800',
        'category': pizza,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
    {
        'name': 'Prosciutto e Funghi',
        'description': 'Tomato sauce, mozzarella, ham, mushrooms',
        'price': 13.50,
        'image': 'https://images.unsplash.com/photo-1571407970349-bc81e7e96f47?w=800',
        'category': pizza,
        'spice_level': 'none',
    },
    {
        'name': 'Napoli',
        'description': 'Tomato sauce, mozzarella, anchovies, capers, olives',
        'price': 12.90,
        'image': 'https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=800',
        'category': pizza,
        'spice_level': 'none',
    },
    {
        'name': 'Calzone',
        'description': 'Folded pizza with ham, mushrooms, mozzarella',
        'price': 13.90,
        'image': 'https://images.unsplash.com/photo-1593504049359-74330189a345?w=800',
        'category': pizza,
        'spice_level': 'none',
    },
]

for item_data in pizzas:
    MenuItem.objects.create(**item_data)
    print(f"  ✅ {item_data['name']}")

# ==================== PASTA ====================
pastas = [
    {
        'name': 'Spaghetti Carbonara',
        'description': 'Spaghetti with eggs, bacon, parmesan, black pepper',
        'price': 12.90,
        'image': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=800',
        'category': pasta,
        'is_featured': True,
        'spice_level': 'none',
    },
    {
        'name': 'Spaghetti Bolognese',
        'description': 'Spaghetti with traditional meat sauce',
        'price': 11.90,
        'image': 'https://images.unsplash.com/photo-1622973536968-3ead9e780960?w=800',
        'category': pasta,
        'spice_level': 'none',
    },
    {
        'name': 'Penne Arrabbiata',
        'description': 'Penne with spicy tomato sauce, garlic, chili',
        'price': 10.90,
        'image': 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=800',
        'category': pasta,
        'is_vegetarian': True,
        'spice_level': 'hot',
    },
    {
        'name': 'Lasagna Bolognese',
        'description': 'Layered pasta with meat sauce, béchamel, parmesan',
        'price': 13.90,
        'image': 'https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=800',
        'category': pasta,
        'spice_level': 'none',
    },
    {
        'name': 'Penne al Salmone',
        'description': 'Penne with salmon, cream sauce, dill',
        'price': 14.90,
        'image': 'https://images.unsplash.com/photo-1611270629569-8b357c1e752f?w=800',
        'category': pasta,
        'spice_level': 'none',
    },
    {
        'name': 'Tagliatelle ai Funghi',
        'description': 'Tagliatelle with mushrooms, cream, parsley',
        'price': 12.50,
        'image': 'https://images.unsplash.com/photo-1598866594230-a7c12756260f?w=800',
        'category': pasta,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
    {
        'name': 'Spaghetti Aglio e Olio',
        'description': 'Spaghetti with garlic, olive oil, chili, parsley',
        'price': 9.90,
        'image': 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=800',
        'category': pasta,
        'is_vegetarian': True,
        'spice_level': 'mild',
    },
]

for item_data in pastas:
    MenuItem.objects.create(**item_data)
    print(f"  ✅ {item_data['name']}")

# ==================== SALADS ====================
salad_items = [
    {
        'name': 'Caesar Salad',
        'description': 'Romaine lettuce, croutons, parmesan, Caesar dressing',
        'price': 8.90,
        'image': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=800',
        'category': salads,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
    {
        'name': 'Mixed Salad',
        'description': 'Fresh mixed greens, tomatoes, cucumber, carrots',
        'price': 6.90,
        'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800',
        'category': salads,
        'is_vegetarian': True,
        'is_vegan': True,
        'spice_level': 'none',
    },
    {
        'name': 'Tuna Salad',
        'description': 'Mixed greens, tuna, tomatoes, olives, onions',
        'price': 10.90,
        'image': 'https://images.unsplash.com/photo-1607532941433-304659e8198a?w=800',
        'category': salads,
        'spice_level': 'none',
    },
]

for item_data in salad_items:
    MenuItem.objects.create(**item_data)
    print(f"  ✅ {item_data['name']}")

# ==================== DESSERTS ====================
dessert_items = [
    {
        'name': 'Tiramisu',
        'description': 'Classic Italian dessert with coffee, mascarpone, cocoa',
        'price': 6.90,
        'image': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=800',
        'category': desserts,
        'is_vegetarian': True,
        'is_featured': True,
        'spice_level': 'none',
    },
    {
        'name': 'Panna Cotta',
        'description': 'Creamy vanilla dessert with berry sauce',
        'price': 5.90,
        'image': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800',
        'category': desserts,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
    {
        'name': 'Tartufo',
        'description': 'Italian ice cream truffle with chocolate coating',
        'price': 6.50,
        'image': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800',
        'category': desserts,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
    {
        'name': 'Affogato',
        'description': 'Vanilla gelato drowned in hot espresso',
        'price': 5.50,
        'image': 'https://images.unsplash.com/photo-1514849302-984523450cf4?w=800',
        'category': desserts,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
]

for item_data in dessert_items:
    MenuItem.objects.create(**item_data)
    print(f"  ✅ {item_data['name']}")

# ==================== BEVERAGES ====================
drinks = [
    {
        'name': 'Coca Cola',
        'description': 'Classic cola drink (330ml)',
        'price': 3.50,
        'image': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=800',
        'category': beverages,
        'is_vegetarian': True,
        'is_vegan': True,
        'spice_level': 'none',
    },
    {
        'name': 'Sprite',
        'description': 'Lemon-lime soda (330ml)',
        'price': 3.50,
        'image': 'https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=800',
        'category': beverages,
        'is_vegetarian': True,
        'is_vegan': True,
        'spice_level': 'none',
    },
    {
        'name': 'Fanta',
        'description': 'Orange soda (330ml)',
        'price': 3.50,
        'image': 'https://images.unsplash.com/photo-1624517452488-04869289c4ca?w=800',
        'category': beverages,
        'is_vegetarian': True,
        'is_vegan': True,
        'spice_level': 'none',
    },
    {
        'name': 'Mineral Water',
        'description': 'Still or sparkling (500ml)',
        'price': 2.50,
        'image': 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=800',
        'category': beverages,
        'is_vegetarian': True,
        'is_vegan': True,
        'spice_level': 'none',
    },
    {
        'name': 'Espresso',
        'description': 'Italian espresso coffee',
        'price': 2.90,
        'image': 'https://images.unsplash.com/photo-1610889556528-9a770e32642f?w=800',
        'category': beverages,
        'is_vegetarian': True,
        'is_vegan': True,
        'spice_level': 'none',
    },
    {
        'name': 'Cappuccino',
        'description': 'Espresso with steamed milk and foam',
        'price': 3.90,
        'image': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=800',
        'category': beverages,
        'is_vegetarian': True,
        'spice_level': 'none',
    },
]

for item_data in drinks:
    MenuItem.objects.create(**item_data)
    print(f"  ✅ {item_data['name']}")

# Statistiques
total_items = MenuItem.objects.count()
print(f"\n🎉 MENU CRÉÉ AVEC SUCCÈS!")
print(f"📊 {total_items} plats ajoutés avec de belles photos")
print(f"\n📋 Répartition:")
print(f"  - Starters: {len(starters)}")
print(f"  - Pizzas: {len(pizzas)}")
print(f"  - Pasta: {len(pastas)}")
print(f"  - Salads: {len(salad_items)}")
print(f"  - Desserts: {len(dessert_items)}")
print(f"  - Beverages: {len(drinks)}")
print(f"\n✅ Votre menu est prêt!")
print(f"🌐 Ouvrez l'app pour voir tous les plats avec photos!")
