# Generated by Django 4.0.4 on 2022-05-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0014_alter_shop_options_alter_shop_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='magazainproduct',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='full_count',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Общее количество продукта'),
        ),
    ]
