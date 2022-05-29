from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator
from datetime import datetime
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, verbose_name='номер телефона')
    brand_member = models.ForeignKey('items.Brand', on_delete=models.SET_NULL, verbose_name='член бренда', related_name='user_brand', null=True, blank=True) # Если пользователь член какого-либо бренда, то может создать продукт на основе бренда, при услоий разрешения.
    shop_member = models.ForeignKey('items.Shop', on_delete=models.SET_NULL, verbose_name='член магазина', related_name='user_shop', null=True, blank=True) 
    status = models.BooleanField(default=False, verbose_name="Статус")
    is_brand_admin = models.BooleanField(default=False, verbose_name="Админ")
    shop_status = models.BooleanField(default=False, verbose_name="Магазин Статус")
    is_shop_admin = models.BooleanField(default=False, verbose_name="Админ Магазина")

    def __str__(self):
        return self.user.username
    @property
    def get_instance(self):
        return self

class HistoryProduct(models.Model):
    name = models.CharField(max_length=100)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    add_time = models.DateField(default=datetime.now, blank=True)
    samovyzov = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    @property
    def dostavleno(self):
        seichas = datetime.today().strftime('%Y-%m-%d')
        a = self.add_time + timedelta(days=1)
        zavtra = str(a)
        if seichas == zavtra and self.samovyzov == False:
            return True
        elif seichas != zavtra and self.samovyzov == False:
            return False
        else:
            return None

class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ManyToManyField(HistoryProduct, null=True, blank=True)
    def __str__(self):
        return self.user.user.username

    @receiver(post_save, sender=Profile)
    def create_or_update_busket(sender, instance, created, **kwargs):
        if created:
            History.objects.create(user=instance)

class CommentProduct(models.Model):
    star = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='комментящий')
    product = models.ForeignKey('items.Product', on_delete=models.CASCADE, verbose_name='комментящий продукт')
    text = models.TextField(validators=[MinLengthValidator(20), MaxLengthValidator(450)], 
                            help_text='Максимальное число символов 450, минимально 20', 
                            verbose_name='комментарий')
    is_aviabale = models.BooleanField(default=False)
    def __str__(self):
        return 'коммент на {}, от {}'.format(self.product, self.user)


class CommentShop(models.Model):
    star = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='комментящий')
    product = models.ForeignKey('items.Shop', on_delete=models.CASCADE, verbose_name='комментящий продукт')
    text = models.TextField(validators=[MinLengthValidator(20), MaxLengthValidator(450)], 
                            help_text='Максимальное число символов 450, минимально 20', 
                            verbose_name='комментарий')
    is_aviabale = models.BooleanField(default=False)
    def __str__(self):
        return 'коммент на {}, от {}'.format(self.product, self.user)