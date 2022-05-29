# Generated by Django 4.0.4 on 2022-05-22 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_status'),
        ('items', '0008_corsina_total_price_product_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.product', verbose_name='Продукт в корзине')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
        migrations.AlterField(
            model_name='corsina',
            name='items',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='busket_product', to='items.cartedproduct', verbose_name='Продукты в корзине'),
        ),
    ]