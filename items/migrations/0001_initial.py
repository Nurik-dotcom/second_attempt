# Generated by Django 4.0.4 on 2022-05-20 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название бренда')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название категорий')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категорий',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_aviabale', models.BooleanField(default=False, verbose_name='Доступность')),
                ('image', models.ImageField(default='default.png', upload_to='', verbose_name='Фото продукта')),
                ('name', models.CharField(max_length=100, verbose_name='Имя продукта')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание продукта')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена продукта')),
                ('full_count', models.PositiveIntegerField(default=0, verbose_name='Общее количество продукта')),
                ('saled', models.PositiveIntegerField(blank=True, null=True, verbose_name='Продано')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.brand', verbose_name='Бренд продукта')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='items.category', verbose_name='Категория продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
    ]
