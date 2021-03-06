# Generated by Django 4.0.4 on 2022-05-27 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0023_magazainproduct_is_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazainproduct',
            name='is_initial',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='magazainproduct',
            name='shop',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.shop'),
        ),
    ]
