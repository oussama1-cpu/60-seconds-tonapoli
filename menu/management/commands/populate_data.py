from django.core.management.base import BaseCommand
from menu.models import (
    Category, MenuItem, Ingredient, MenuItemIngredient,
    Customization, RestaurantInfo
)
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populates the database with sample restaurant data'

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data for Restaurant Menu API...")
        self.stdout.write("=" * 50)

        # Create Restaurant Info
        self.stdout.write("\n1. Creating Restaurant Information...")
        restaurant_info, created = RestaurantInfo.objects.get_or_create(
            id=1,
            defaults={
                'name': '60 Seconds to Napoli',
                'description': 'Authentic Italian cuisine with a modern twist. Experience the taste of Naples in every bite.',
                'phone': '+39 081 123 4567',
                'email': 'info@60secondstonapoli.com',
                'address': 'Via Roma 123, 80100 Napoli, Italy',
                'opening_hours': 'Monday-Friday: 11:00-23:00\nSaturday-Sunday: 10:00-00:00',
                'currency_symbol': '€',
                'tax_rate': Decimal('22.00'),
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS("   ✓ Restaurant info created"))
        else:
            self.stdout.write("   ℹ Restaurant info already exists")

        # Create Categories
        self.stdout.write("\n2. Creating Categories...")
        categories_data = [
            {'name': 'Appetizers', 'description': 'Start your meal with our delicious starters', 'order': 1},
            {'name': 'Pizzas', 'description': 'Traditional Neapolitan pizzas baked in wood-fired oven', 'order': 2},
            {'name': 'Pasta', 'description': 'Fresh homemade pasta dishes', 'order': 3},
            {'name': 'Main Courses', 'description': 'Hearty Italian main dishes', 'order': 4},
            {'name': 'Desserts', 'description': 'Sweet endings to your meal', 'order': 5},
            {'name': 'Drinks', 'description': 'Beverages and cocktails', 'order': 6},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created category: {cat_data['name']}"))
            else:
                self.stdout.write(f"   ℹ Category exists: {cat_data['name']}")

        # Create Ingredients
        self.stdout.write("\n3. Creating Ingredients...")
        ingredients_data = [
            {'name': 'Tomato Sauce', 'is_allergen': False},
            {'name': 'Mozzarella', 'is_allergen': True},
            {'name': 'Basil', 'is_allergen': False},
            {'name': 'Olive Oil', 'is_allergen': False},
            {'name': 'Parmesan', 'is_allergen': True},
            {'name': 'Eggs', 'is_allergen': True},
            {'name': 'Bacon', 'is_allergen': False},
            {'name': 'Garlic', 'is_allergen': False},
            {'name': 'Mushrooms', 'is_allergen': False},
            {'name': 'Pepperoni', 'is_allergen': False},
            {'name': 'Ricotta', 'is_allergen': True},
            {'name': 'Spinach', 'is_allergen': False},
        ]

        ingredients = {}
        for ing_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ing_data['name'],
                defaults=ing_data
            )
            ingredients[ing_data['name']] = ingredient
            if created:
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created ingredient: {ing_data['name']}"))

        # Create Menu Items
        self.stdout.write("\n4. Creating Menu Items...")

        # Appetizers
        appetizers = [
            {
                'name': 'Bruschetta',
                'description': 'Toasted bread topped with fresh tomatoes, garlic, basil, and olive oil',
                'price': Decimal('6.99'),
                'is_vegetarian': True,
                'is_vegan': True,
                'preparation_time': 10,
                'calories': 180,
            },
            {
                'name': 'Caprese Salad',
                'description': 'Fresh mozzarella, tomatoes, and basil with balsamic glaze',
                'price': Decimal('8.99'),
                'is_vegetarian': True,
                'preparation_time': 5,
                'calories': 220,
            },
            {
                'name': 'Garlic Bread',
                'description': 'Crispy bread with garlic butter and herbs',
                'price': Decimal('4.99'),
                'is_vegetarian': True,
                'preparation_time': 8,
                'calories': 280,
            },
        ]

        for item_data in appetizers:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                category=categories['Appetizers'],
                defaults={**item_data, 'is_available': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created: {item_data['name']}"))

        # Pizzas
        pizzas = [
            {
                'name': 'Margherita',
                'description': 'Classic pizza with tomato sauce, mozzarella, and fresh basil',
                'price': Decimal('10.99'),
                'is_vegetarian': True,
                'is_featured': True,
                'preparation_time': 15,
                'calories': 800,
            },
            {
                'name': 'Pepperoni',
                'description': 'Tomato sauce, mozzarella, and spicy pepperoni',
                'price': Decimal('12.99'),
                'spice_level': 1,
                'preparation_time': 15,
                'calories': 950,
            },
            {
                'name': 'Quattro Formaggi',
                'description': 'Four cheese pizza: mozzarella, gorgonzola, parmesan, and ricotta',
                'price': Decimal('13.99'),
                'is_vegetarian': True,
                'preparation_time': 15,
                'calories': 1100,
            },
            {
                'name': 'Diavola',
                'description': 'Spicy salami, hot peppers, tomato sauce, and mozzarella',
                'price': Decimal('13.99'),
                'spice_level': 3,
                'is_featured': True,
                'preparation_time': 15,
                'calories': 980,
            },
            {
                'name': 'Vegetariana',
                'description': 'Grilled vegetables, mushrooms, peppers, and mozzarella',
                'price': Decimal('11.99'),
                'is_vegetarian': True,
                'is_vegan': False,
                'preparation_time': 18,
                'calories': 750,
            },
        ]

        for item_data in pizzas:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                category=categories['Pizzas'],
                defaults={**item_data, 'is_available': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created: {item_data['name']}"))

        # Pasta
        pastas = [
            {
                'name': 'Spaghetti Carbonara',
                'description': 'Classic Roman pasta with eggs, bacon, parmesan, and black pepper',
                'price': Decimal('12.99'),
                'preparation_time': 20,
                'calories': 850,
            },
            {
                'name': 'Penne Arrabbiata',
                'description': 'Penne pasta in spicy tomato sauce with garlic and chili',
                'price': Decimal('10.99'),
                'is_vegetarian': True,
                'is_vegan': True,
                'spice_level': 2,
                'preparation_time': 18,
                'calories': 680,
            },
            {
                'name': 'Lasagna',
                'description': 'Layers of pasta with meat sauce, béchamel, and cheese',
                'price': Decimal('14.99'),
                'is_featured': True,
                'preparation_time': 25,
                'calories': 1200,
            },
            {
                'name': 'Fettuccine Alfredo',
                'description': 'Creamy parmesan sauce with fettuccine pasta',
                'price': Decimal('11.99'),
                'is_vegetarian': True,
                'preparation_time': 15,
                'calories': 920,
            },
        ]

        for item_data in pastas:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                category=categories['Pasta'],
                defaults={**item_data, 'is_available': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created: {item_data['name']}"))

        # Main Courses
        mains = [
            {
                'name': 'Chicken Parmigiana',
                'description': 'Breaded chicken breast with tomato sauce and melted mozzarella',
                'price': Decimal('16.99'),
                'preparation_time': 30,
                'calories': 980,
            },
            {
                'name': 'Osso Buco',
                'description': 'Braised veal shanks with vegetables and white wine',
                'price': Decimal('22.99'),
                'is_featured': True,
                'preparation_time': 45,
                'calories': 850,
            },
            {
                'name': 'Grilled Salmon',
                'description': 'Fresh salmon fillet with lemon butter sauce and vegetables',
                'price': Decimal('18.99'),
                'is_gluten_free': True,
                'preparation_time': 25,
                'calories': 650,
            },
        ]

        for item_data in mains:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                category=categories['Main Courses'],
                defaults={**item_data, 'is_available': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created: {item_data['name']}"))

        # Desserts
        desserts = [
            {
                'name': 'Tiramisu',
                'description': 'Classic Italian dessert with coffee-soaked ladyfingers and mascarpone',
                'price': Decimal('6.99'),
                'is_vegetarian': True,
                'is_featured': True,
                'preparation_time': 10,
                'calories': 450,
            },
            {
                'name': 'Panna Cotta',
                'description': 'Creamy vanilla custard with berry sauce',
                'price': Decimal('5.99'),
                'is_vegetarian': True,
                'is_gluten_free': True,
                'preparation_time': 8,
                'calories': 320,
            },
            {
                'name': 'Gelato',
                'description': 'Italian ice cream - ask for available flavors',
                'price': Decimal('4.99'),
                'is_vegetarian': True,
                'is_gluten_free': True,
                'preparation_time': 2,
                'calories': 250,
            },
        ]

        for item_data in desserts:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                category=categories['Desserts'],
                defaults={**item_data, 'is_available': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created: {item_data['name']}"))

        # Drinks
        drinks = [
            {
                'name': 'Espresso',
                'description': 'Strong Italian coffee',
                'price': Decimal('2.50'),
                'is_vegetarian': True,
                'is_vegan': True,
                'is_gluten_free': True,
                'preparation_time': 3,
                'calories': 5,
            },
            {
                'name': 'Cappuccino',
                'description': 'Espresso with steamed milk and foam',
                'price': Decimal('3.50'),
                'is_vegetarian': True,
                'preparation_time': 5,
                'calories': 120,
            },
            {
                'name': 'Italian Soda',
                'description': 'Sparkling water with fruit syrup',
                'price': Decimal('3.99'),
                'is_vegetarian': True,
                'is_vegan': True,
                'preparation_time': 2,
                'calories': 150,
            },
            {
                'name': 'House Wine (Glass)',
                'description': 'Red or white wine from our selection',
                'price': Decimal('5.99'),
                'is_vegetarian': True,
                'is_vegan': True,
                'is_gluten_free': True,
                'preparation_time': 1,
                'calories': 125,
            },
        ]

        for item_data in drinks:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                category=categories['Drinks'],
                defaults={**item_data, 'is_available': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created: {item_data['name']}"))

        # Create Customizations
        self.stdout.write("\n5. Creating Customizations...")
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
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created customization: {custom_data['name']}"))

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("✅ Sample data creation completed!"))
        self.stdout.write("\nSummary:")
        self.stdout.write(f"   Categories: {Category.objects.count()}")
        self.stdout.write(f"   Menu Items: {MenuItem.objects.count()}")
        self.stdout.write(f"   Ingredients: {Ingredient.objects.count()}")
        self.stdout.write(f"   Customizations: {Customization.objects.count()}")
        self.stdout.write("\nYou can now:")
        self.stdout.write("   1. Access admin at: http://127.0.0.1:8000/admin/")
        self.stdout.write("   2. View API at: http://127.0.0.1:8000/api/")
        self.stdout.write("   3. Check docs at: http://127.0.0.1:8000/swagger/")
        self.stdout.write("=" * 50)
