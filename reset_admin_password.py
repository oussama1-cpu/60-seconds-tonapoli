from django.contrib.auth import get_user_model

User = get_user_model()

# Get or create superuser
username = "admin"
email = "admin@napoli.com"
password = "admin123"

try:
    # Try to get existing superuser
    user = User.objects.filter(is_superuser=True).first()
    
    if user:
        # Update existing user
        user.username = username
        user.email = email
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        print(f"✅ Password reset successful!")
    else:
        # Create new superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser created!")
    
    print(f"\n{'='*50}")
    print(f"🔐 SUPERADMIN LOGIN CREDENTIALS")
    print(f"{'='*50}")
    print(f"URL:      http://127.0.0.1:8000/admin/")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"{'='*50}\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
