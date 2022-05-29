# Generated by Django 4.0.4 on 2022-05-21 09:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_status'),
        ('items', '0005_corsina'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('text', models.TextField(help_text='Максимальное число символов 450, минимально 20', validators=[django.core.validators.MinLengthValidator(20), django.core.validators.MaxLengthValidator(450)], verbose_name='комментарий')),
                ('is_aviabale', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.product', verbose_name='комментящий продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='комментящий')),
            ],
        ),
    ]
