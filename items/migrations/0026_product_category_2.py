# Generated by Django 4.0.4 on 2022-05-27 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0025_category2'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='items.category2'),
        ),
    ]
