# Generated by Django 4.0.4 on 2022-05-21 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corsina',
            name='items',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='busket_product', to='items.product', verbose_name='Продукты в корзине'),
        ),
    ]
