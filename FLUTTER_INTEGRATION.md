# Flutter Integration Guide

Complete guide for integrating this Django REST API with your Flutter application.

## 📦 Flutter Dependencies

Add these to your `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  provider: ^6.0.5
  cached_network_image: ^3.3.0
  intl: ^0.18.1
```

## 🔧 API Service Setup

### 1. Create API Configuration

Create `lib/config/api_config.dart`:

```dart
class ApiConfig {
  // Change based on your environment
  static const String baseUrl = 'http://10.0.2.2:8000/api'; // Android Emulator
 
  
  static const String categoriesEndpoint = '/categories/';
  static const String menuItemsEndpoint = '/menu-items/';
  static const String restaurantInfoEndpoint = '/restaurant-info/current/';
  static const String reviewsEndpoint = '/reviews/';
}
```

### 2. Create Data Models

Create `lib/models/category.dart`:

```dart
class Category {
  final int id;
  final String name;
  final String description;
  final String? image;
  final int order;
  final bool isActive;
  final int itemCount;

  Category({
    required this.id,
    required this.name,
    required this.description,
    this.image,
    required this.order,
    required this.isActive,
    required this.itemCount,
  });

  factory Category.fromJson(Map<String, dynamic> json) {
    return Category(
      id: json['id'],
      name: json['name'],
      description: json['description'] ?? '',
      image: json['image'],
      order: json['order'],
      isActive: json['is_active'],
      itemCount: json['item_count'] ?? 0,
    );
  }
}
```

Create `lib/models/menu_item.dart`:

```dart
class MenuItem {
  final int id;
  final String name;
  final String description;
  final int categoryId;
  final String categoryName;
  final String price;
  final String? image;
  final String spiceLevel;
  final bool isVegetarian;
  final bool isVegan;
  final bool isGlutenFree;
  final bool containsNuts;
  final bool isAvailable;
  final bool isFeatured;
  final int? preparationTime;
  final int? calories;
  final double? averageRating;

  MenuItem({
    required this.id,
    required this.name,
    required this.description,
    required this.categoryId,
    required this.categoryName,
    required this.price,
    this.image,
    required this.spiceLevel,
    required this.isVegetarian,
    required this.isVegan,
    required this.isGlutenFree,
    required this.containsNuts,
    required this.isAvailable,
    required this.isFeatured,
    this.preparationTime,
    this.calories,
    this.averageRating,
  });

  factory MenuItem.fromJson(Map<String, dynamic> json) {
    return MenuItem(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      categoryId: json['category'],
      categoryName: json['category_name'] ?? '',
      price: json['price'],
      image: json['image'],
      spiceLevel: json['spice_level'],
      isVegetarian: json['is_vegetarian'],
      isVegan: json['is_vegan'],
      isGlutenFree: json['is_gluten_free'],
      containsNuts: json['contains_nuts'],
      isAvailable: json['is_available'],
      isFeatured: json['is_featured'],
      preparationTime: json['preparation_time'],
      calories: json['calories'],
      averageRating: json['average_rating']?.toDouble(),
    );
  }

  String get priceFormatted => '€$price';
  
  List<String> get dietaryBadges {
    List<String> badges = [];
    if (isVegetarian) badges.add('Vegetarian');
    if (isVegan) badges.add('Vegan');
    if (isGlutenFree) badges.add('Gluten-Free');
    if (containsNuts) badges.add('Contains Nuts');
    return badges;
  }
}
```

### 3. Create API Service

Create `lib/services/menu_api_service.dart`:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/category.dart';
import '../models/menu_item.dart';

class MenuApiService {
  // Get all categories
  Future<List<Category>> getCategories() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.categoriesEndpoint}'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List results = data['results'];
        return results.map((json) => Category.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load categories');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // Get all menu items
  Future<List<MenuItem>> getMenuItems({int? categoryId}) async {
    try {
      String url = '${ApiConfig.baseUrl}${ApiConfig.menuItemsEndpoint}';
      if (categoryId != null) {
        url += '?category=$categoryId';
      }

      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List results = data['results'];
        return results.map((json) => MenuItem.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load menu items');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // Get featured items
  Future<List<MenuItem>> getFeaturedItems() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.menuItemsEndpoint}featured/'),
      );

      if (response.statusCode == 200) {
        final List data = json.decode(response.body);
        return data.map((json) => MenuItem.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load featured items');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // Search menu items
  Future<List<MenuItem>> searchMenuItems(String query) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.menuItemsEndpoint}search/?q=$query'),
      );

      if (response.statusCode == 200) {
        final List data = json.decode(response.body);
        return data.map((json) => MenuItem.fromJson(json)).toList();
      } else {
        throw Exception('Failed to search menu items');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // Get menu item details
  Future<Map<String, dynamic>> getMenuItemDetails(int id) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.menuItemsEndpoint}$id/'),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load menu item details');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // Submit a review
  Future<void> submitReview({
    required int menuItemId,
    required String customerName,
    required int rating,
    String? comment,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.reviewsEndpoint}'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'menu_item': menuItemId,
          'customer_name': customerName,
          'rating': rating,
          'comment': comment ?? '',
        }),
      );

      if (response.statusCode != 201) {
        throw Exception('Failed to submit review');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // Get restaurant info
  Future<Map<String, dynamic>> getRestaurantInfo() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.restaurantInfoEndpoint}'),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load restaurant info');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}
```

## 🎨 Example UI Screens

### 1. Categories Screen

```dart
import 'package:flutter/material.dart';
import '../services/menu_api_service.dart';
import '../models/category.dart';

class CategoriesScreen extends StatefulWidget {
  @override
  _CategoriesScreenState createState() => _CategoriesScreenState();
}

class _CategoriesScreenState extends State<CategoriesScreen> {
  final MenuApiService _apiService = MenuApiService();
  late Future<List<Category>> _categoriesFuture;

  @override
  void initState() {
    super.initState();
    _categoriesFuture = _apiService.getCategories();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Menu Categories'),
      ),
      body: FutureBuilder<List<Category>>(
        future: _categoriesFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No categories found'));
          }

          final categories = snapshot.data!;

          return GridView.builder(
            padding: EdgeInsets.all(16),
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              childAspectRatio: 0.85,
            ),
            itemCount: categories.length,
            itemBuilder: (context, index) {
              final category = categories[index];
              return CategoryCard(category: category);
            },
          );
        },
      ),
    );
  }
}

class CategoryCard extends StatelessWidget {
  final Category category;

  const CategoryCard({required this.category});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        onTap: () {
          // Navigate to menu items screen
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => MenuItemsScreen(categoryId: category.id),
            ),
          );
        },
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(
              child: ClipRRect(
                borderRadius: BorderRadius.vertical(top: Radius.circular(12)),
                child: category.image != null
                    ? Image.network(
                        category.image!,
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) {
                          return Container(
                            color: Colors.grey[300],
                            child: Icon(Icons.restaurant, size: 50),
                          );
                        },
                      )
                    : Container(
                        color: Colors.grey[300],
                        child: Icon(Icons.restaurant, size: 50),
                      ),
              ),
            ),
            Padding(
              padding: EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    category.name,
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  SizedBox(height: 4),
                  Text(
                    '${category.itemCount} items',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

### 2. Menu Items Screen

```dart
import 'package:flutter/material.dart';
import '../services/menu_api_service.dart';
import '../models/menu_item.dart';

class MenuItemsScreen extends StatefulWidget {
  final int? categoryId;

  const MenuItemsScreen({this.categoryId});

  @override
  _MenuItemsScreenState createState() => _MenuItemsScreenState();
}

class _MenuItemsScreenState extends State<MenuItemsScreen> {
  final MenuApiService _apiService = MenuApiService();
  late Future<List<MenuItem>> _menuItemsFuture;

  @override
  void initState() {
    super.initState();
    _menuItemsFuture = _apiService.getMenuItems(categoryId: widget.categoryId);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Menu Items'),
        actions: [
          IconButton(
            icon: Icon(Icons.search),
            onPressed: () {
              // Implement search
            },
          ),
        ],
      ),
      body: FutureBuilder<List<MenuItem>>(
        future: _menuItemsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No menu items found'));
          }

          final items = snapshot.data!;

          return ListView.builder(
            padding: EdgeInsets.all(16),
            itemCount: items.length,
            itemBuilder: (context, index) {
              return MenuItemCard(item: items[index]);
            },
          );
        },
      ),
    );
  }
}

class MenuItemCard extends StatelessWidget {
  final MenuItem item;

  const MenuItemCard({required this.item});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.only(bottom: 16),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        onTap: () {
          // Navigate to item details
        },
        child: Padding(
          padding: EdgeInsets.all(12),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Image
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: item.image != null
                    ? Image.network(
                        item.image!,
                        width: 100,
                        height: 100,
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) {
                          return Container(
                            width: 100,
                            height: 100,
                            color: Colors.grey[300],
                            child: Icon(Icons.restaurant),
                          );
                        },
                      )
                    : Container(
                        width: 100,
                        height: 100,
                        color: Colors.grey[300],
                        child: Icon(Icons.restaurant),
                      ),
              ),
              SizedBox(width: 12),
              // Details
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      item.name,
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      item.description,
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey[600],
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    SizedBox(height: 8),
                    // Dietary badges
                    Wrap(
                      spacing: 4,
                      children: item.dietaryBadges.map((badge) {
                        return Chip(
                          label: Text(
                            badge,
                            style: TextStyle(fontSize: 10),
                          ),
                          padding: EdgeInsets.zero,
                          materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                        );
                      }).toList(),
                    ),
                    SizedBox(height: 8),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          item.priceFormatted,
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Theme.of(context).primaryColor,
                          ),
                        ),
                        if (item.averageRating != null)
                          Row(
                            children: [
                              Icon(Icons.star, color: Colors.amber, size: 16),
                              SizedBox(width: 4),
                              Text(
                                item.averageRating!.toStringAsFixed(1),
                                style: TextStyle(fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

## 🚀 Testing the Integration

1. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

2. **Update API URL in Flutter:**
   - Android Emulator: `http://10.0.2.2:8000/api`
   - iOS Simulator: `http://localhost:8000/api`
   - Physical Device: `http://YOUR_COMPUTER_IP:8000/api`

3. **Run Flutter app:**
   ```bash
   flutter run
   ```

## 🔍 Debugging Tips

### Check API Connection
```dart
Future<void> testConnection() async {
  try {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/categories/'),
    );
    print('Status Code: ${response.statusCode}');
    print('Response: ${response.body}');
  } catch (e) {
    print('Error: $e');
  }
}
```

### Common Issues

1. **Connection refused**: Make sure Django server is running
2. **CORS errors**: Check Django CORS settings
3. **Images not loading**: Use full URL with domain
4. **Timeout errors**: Check network connectivity

## 📱 Complete Example App Structure

```
lib/
├── config/
│   └── api_config.dart
├── models/
│   ├── category.dart
│   ├── menu_item.dart
│   └── restaurant_info.dart
├── services/
│   └── menu_api_service.dart
├── screens/
│   ├── categories_screen.dart
│   ├── menu_items_screen.dart
│   ├── item_details_screen.dart
│   └── search_screen.dart
├── widgets/
│   ├── category_card.dart
│   ├── menu_item_card.dart
│   └── dietary_badge.dart
└── main.dart
```

## 🎉 You're Ready!

Your Flutter app is now connected to the Django API. Start building your restaurant menu app!
