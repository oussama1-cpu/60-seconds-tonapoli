"""
Script de test pour vérifier que le CRUD fonctionne avec l'API Django
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_create_menu_item():
    """Test création d'un menu item"""
    print("\n" + "="*60)
    print("TEST 1: CRÉER UN MENU ITEM")
    print("="*60)
    
    data = {
        "name": "Test Pizza CRUD",
        "description": "Pizza de test pour vérifier le CRUD",
        "price": "15.99",
        "category": 1,  # ID de la catégorie Pizza
        "is_available": True,
        "is_featured": False,
        "is_vegetarian": True,
        "is_vegan": False,
        "is_gluten_free": False,
        "spice_level": "none",  # Options: none, mild, medium, hot
        "contains_nuts": False,
    }
    
    try:
        response = requests.post(f"{BASE_URL}/menu-items/", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ SUCCESS! Menu item créé:")
            print(json.dumps(result, indent=2))
            return result.get('id')
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None


def test_update_menu_item(item_id):
    """Test modification d'un menu item"""
    print("\n" + "="*60)
    print("TEST 2: MODIFIER LE MENU ITEM")
    print("="*60)
    
    data = {
        "name": "Test Pizza CRUD MODIFIÉE",
        "description": "Description modifiée pour test",
        "price": "18.99",
        "category": 1,
        "is_available": True,
        "is_featured": True,
        "is_vegetarian": True,
        "is_vegan": False,
        "is_gluten_free": False,
        "spice_level": "medium",  # Options: none, mild, medium, hot
        "contains_nuts": False,
    }
    
    try:
        response = requests.put(f"{BASE_URL}/menu-items/{item_id}/", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Menu item modifié:")
            print(json.dumps(result, indent=2))
            return True
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_get_menu_items():
    """Test lecture des menu items"""
    print("\n" + "="*60)
    print("TEST 3: LIRE TOUS LES MENU ITEMS")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/menu-items/")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            count = result.get('count', len(result))
            print(f"✅ SUCCESS! {count} menu items trouvés")
            
            # Afficher les 5 premiers
            items = result.get('results', result)
            for item in items[:5]:
                print(f"  - {item.get('name')} (€{item.get('price')})")
            return True
        else:
            print(f"❌ FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_delete_menu_item(item_id):
    """Test suppression d'un menu item"""
    print("\n" + "="*60)
    print("TEST 4: SUPPRIMER LE MENU ITEM")
    print("="*60)
    
    try:
        response = requests.delete(f"{BASE_URL}/menu-items/{item_id}/")
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print("✅ SUCCESS! Menu item supprimé")
            return True
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("🧪 TEST COMPLET DU CRUD API")
    print("="*60)
    print("\nServeur Django doit tourner sur: http://127.0.0.1:8000")
    print("Credentials: admin / admin123")
    print("\n" + "="*60)
    
    # Test Read first
    test_get_menu_items()
    
    # Test Create
    item_id = test_create_menu_item()
    
    if item_id:
        # Test Update
        test_update_menu_item(item_id)
        
        # Test Delete
        test_delete_menu_item(item_id)
    
    # Final summary
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    print("""
    Si tous les tests montrent ✅ SUCCESS:
    → Le CRUD fonctionne parfaitement!
    → Vous pouvez maintenant utiliser le SuperAdmin Panel dans Flutter
    
    Si des tests montrent ❌ FAILED:
    → Vérifiez que Django tourne sur le port 8000
    → Vérifiez les permissions dans Django
    → Regardez les logs Django pour plus d'infos
    """)
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
