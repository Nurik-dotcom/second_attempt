# Generated by Django 4.0.4 on 2022-05-28 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0029_product_is_aviabale'),
    ]

    operations = [
        migrations.AddField(
            model_name='maincategory',
            name='subcategory',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='subcategory', to='items.category'),
        ),
    ]
