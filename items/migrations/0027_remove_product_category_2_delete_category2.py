# Generated by Django 4.0.4 on 2022-05-28 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0026_product_category_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category_2',
        ),
        migrations.DeleteModel(
            name='Category2',
        ),
    ]
