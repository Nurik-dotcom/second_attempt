from django import forms
from .models import *
from users.models import *
from django.forms.widgets import TextInput

class CategoryForms(forms.ModelForm):
    class Meta:
        model = Category
        fields=['title',]
class ProductForm(forms.ModelForm):
#     def init(self, *args, **kwargs):
#         self.request = kwargs.pop("request")
#         super(ProductForm, self).init(*args, **kwargs)
#         self.fields["brand"].queryset = Product.objects.filter(brand=self.request.user.profile.brand_member)
# #     # authorID = forms.ModelChoiceField(queryset=Teacher.objects.all(),empty_label="Author", to_field_name="id")
    category=CategoryForms
    class Meta:
        model=Product
        fields=['image' ,'name', 'category', 'description']

# class ForFilter(forms.ModelForm):
#     category=CategoryForms
#     class Meta:
#         model=Product
#         fields=['name', 'category']

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Поиск по Названию'}))
    category = 'ShopCategory'
    class Meta:
        model = Product
        fields = ['name', 'category']

class UpdateForm(forms.ModelForm):
    class Meta:
        model = MagazainProduct
        fields = ['price', 'count']

class UpdateProductForm(forms.ModelForm):
    category =CategoryForms
    class Meta:
        model = Product
        fields = ['image', 'name', 'category', 'description']




class ShopMainCategory(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ['title',]

class ShopCategory(forms.ModelForm):
    maincategory = ShopMainCategory
    class Meta:
        model = Category
        fields = ['title', 'maincategory']

class BrandShop(forms.ModelForm):
    class Meta:
        model=Brand
        fields = ['title', ]

class SvoistcaShop(forms.ModelForm):
    class Meta:
        model = Svoistva
        fields = ['title',]



class CreateShopProductForm(forms.ModelForm):
    category =ShopCategory
    brand=BrandShop
    svoistva = SvoistcaShop
    class Meta:
        model = Product
        fields = ['image', 'name', 'category', 'description', 'brand', 'svoistva']
    
class formainCategory(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ['title',]

class forCategory(forms.ModelForm):
    maincategory = formainCategory
    class Meta:
        model = Category
        fields = ['title','maincategory']

class ProductSubFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Поиск по Названию'}))
    category = forCategory
    class Meta:
        model = Product
        fields = ['name', 'category']
