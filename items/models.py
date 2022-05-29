
from datetime import datetime
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from users.models import *
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator
import django_filters

# Create your models here.

class MainCategory(models.Model):
    subcategory = models.ManyToManyField('Category', null=True, blank=True, default=None, related_name='subcategory')
    title = models.CharField(max_length=100, verbose_name='Название категорий')
    slug = models.SlugField(unique=True, default='Slug')
    def get_absolute_url(self):
        return reverse('maincategory_detail', kwargs={'slug': self.slug})
    def __str__(self):
        return self.title
    
class Category(models.Model):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100, verbose_name='Название категорий')
    slug = models.SlugField(unique=True, default='Slug')
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
    def __str__(self):
        return '{} - {}'.format(self.maincategory.title, self.title)

    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категорий'

class Brand(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название бренда')
    # member = models.ManyToManyField('users.Profile', verbose_name='Член бренда', null=True, blank=True)
    slug = models.SlugField(unique=True, default='Slug')
    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'slug': self.slug})
    def __str__(self):
        return self.title  
    
    class Meta:
        verbose_name='Бренд'
        verbose_name_plural='Бренды'

class Svoistva(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default='Slug')
    def __str__(self):
        return self.title


class Product(models.Model):
    is_aviabale = models.BooleanField(default=False, verbose_name='Доступность')
    quantity = models.PositiveIntegerField(default=1, editable=False)
    image = models.ImageField(default='default.png', verbose_name='Фото продукта')
    name = models.CharField(max_length=100, verbose_name='Имя продукта')
    description = models.TextField(verbose_name='Описание продукта', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, 
                                    blank=True, verbose_name='Категория продукта')                
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд продукта')
    full_count = models.PositiveIntegerField(verbose_name='Общее количество продукта', default=0)
    saled = models.PositiveIntegerField(verbose_name='Продано', null=True, blank=True)
    svoistva = models.ForeignKey(Svoistva, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    add_time = models.DateField(editable=False, default=datetime.now)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    # @property
    # def persentage(self):
    #         return round(self.saled / self.full_count) * 100
            
    def __str__(self):
        return '{} {}'.format(self.category, self.name)
    
    class Meta:
        verbose_name='Продукт'
        verbose_name_plural='Продукты'

    @property
    def price(self):
        prices = []

        my_magazain = MagazainProduct.objects.filter(product_id=self.id, is_initial=False).order_by('price')
        for i in my_magazain:
            prices.append(i.price)
            return str(prices[0])


class Shop(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название магазина')
    slug = models.SlugField(unique=True, default='Slug')
    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'slug': self.slug})
    def __str__(self):
        return self.title  
    
    class Meta:
        verbose_name='Магазин'
        verbose_name_plural='Магазины' 
       
class MagazainProduct(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default=None, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=100)
    is_aviable = models.BooleanField(default=True)
    is_initial = models.BooleanField(default=True)
    def __str__(self):
        return '{}, {}'.format(self.count, self.product.name)

    @receiver(post_save, sender=Product)
    def create_or_update_MagazainProduct(sender, instance, created, **kwargs):
        if created:
            MagazainProduct.objects.create(product=instance)
    
class CartedProduct(models.Model):
    samovyzov = models.BooleanField(default=False, verbose_name='Самовызов')
    product = models.ForeignKey(MagazainProduct, on_delete=models.SET_NULL, verbose_name='Продукт в корзине', 
                                null=True, blank=True)
    count = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    user= models.ForeignKey(Profile, on_delete=models.CASCADE)
    # def __str__(self):
    #     return '{} {}'.format(self.product.product.name, self.user.user.username)

class Corsina(models.Model):
    items = models.ManyToManyField(CartedProduct, null=True, blank=True, 
                                        verbose_name='Продукты в корзине', 
                                        related_name='busket_product', 
                                        default=None)

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, 
                                        verbose_name='Пользователь')
    total_price = models.PositiveIntegerField(default=0, editable=False)
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural='Корзины'
    
    # def __str__(self):
    #     return self.user
    def __str__(self):
        return '{}, {}'.format(self.total_price, self.user.user.username)

    @receiver(post_save, sender=Profile)
    def create_or_update_busket(sender, instance, created, **kwargs):
        if created:
            Corsina.objects.create(user=instance)
