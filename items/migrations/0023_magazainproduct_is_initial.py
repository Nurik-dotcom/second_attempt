# Generated by Django 4.0.4 on 2022-05-26 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0022_alter_product_full_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='magazainproduct',
            name='is_initial',
            field=models.BooleanField(default=False),
        ),
    ]
