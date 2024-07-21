from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def set_default_owner(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    User = apps.get_model(settings.AUTH_USER_MODEL)
    default_user, created = User.objects.get_or_create(
        email='default@example.com',
        defaults={'password': 'defaultpassword123'}  # Измените пароль и другие поля по мере необходимости
    )
    for product in Product.objects.filter(owner__isnull=True):
        product.owner = default_user
        product.save()

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0007_product_owner_version_delete_version_and_more'),
    ]

    operations = [
        migrations.RunPython(set_default_owner),
        migrations.AlterField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
