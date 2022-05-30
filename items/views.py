from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import user_passes_test
# from django.views.generic.edit import CreateView
from django.contrib.auth.models import User, Group

from users.views import *
from .models import Product, Brand, Corsina, CartedProduct, Shop, MagazainProduct, Category, MainCategory
from users import models
from .forms import *
# Home  Page

def home(request):
    products = 0
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()
    categories = MainCategory.objects.all()[:8]
    brands = Svoistva.objects.all()[:6]

    context = {'categories' : categories, 'profile' : profile, 'products':products, 'brands' : brands}
    return render(request, 'home.html', context)

def main(request):
    brands = Svoistva.objects.all()[:6]
    products = 0
    f = ProductFilter(request.GET, queryset=Product.objects.filter(is_aviabale=True))
    categories = MainCategory.objects.all()[:8]
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()

    context = {'filter': f, 'categories' : categories, 'products' : products, 'brands' : brands}
    return render(request, 'main_page.html', context)

# For Category
def category_products(request, slug):
    brands = Svoistva.objects.all()[:6]
    categor_title = MainCategory.objects.get(slug = slug)
    categories = MainCategory.objects.all()[:8]
    # f = ProductSearch(request.GET, queryset=Product.objects.filter(is_aviabale=True, category__slug=slug))
    f = ProductSubFilter(request.GET, queryset=Product.objects.filter(category__maincategory__slug=slug, is_aviabale=True))

    products=0
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()
    return render(request, 'category_products.html', {'filter' : f,'categories' : categories, 'products' : products, 'categor_title': categor_title,'brands' : brands})

def subcategoryProducts(request, slug):
    brands = Svoistva.objects.all()[:6]
    categor_title = Category.objects.get(slug = slug)
    categories = MainCategory.objects.all()[:8]
    f = ProductFilter(request.GET, queryset=Product.objects.filter(category__slug=slug,  is_aviabale=True))

    products=0
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()
    return render(request, 'subcategory_products.html', {'filter' : f,'categories' : categories, 'products' : products, 'categor_title': categor_title,'brands' : brands})

def svoisvtaProducts(request, slug):
    brands = Svoistva.objects.all()[:6]
    categor_title = Svoistva.objects.get(slug = slug)
    categories = MainCategory.objects.all()[:8]
    f = ProductFilter(request.GET, queryset=Product.objects.filter(svoistva__slug=slug,  is_aviabale=True))

    products=0
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()
    return render(request, 'svoistva_products.html', {'filter' : f,'categories' : categories, 'products' : products, 'categor_title': categor_title,'brands' : brands})



def create_product(request):
    product = ProductForm()
    if request.method=='POST':
        product = ProductForm(request.POST,  request.FILES)
        if product.is_valid():
            products=product.save(commit=False)
            try:
                profile = Profile.objects.get(user=request.user)
                brands = profile.brand_member
            except:
                brands = Brand.objects.get(id=1)
            products.brand = brands
            products.save()
        return redirect('homepage')
    return render(request, 'create_product.html', {'form' : ProductForm})


# Product Detail

def product_detail(request, pk):
    brands = Svoistva.objects.all()[:6]
    categories = MainCategory.objects.all()[:8]
    product = Product.objects.get(id=pk)
    products=0
    comment = CommentProduct.objects.filter(product_id=product.id)
    select = MagazainProduct.objects.filter(product=product, is_aviable=False, is_initial=False)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()
    return render(request, 'product_detail.html', {'i' : product,'select' : select, 'categories' : categories, 'products' : products,'brands' : brands})


# Corsina
from django.contrib.auth.decorators import login_required

@login_required
def add_to_corsina(request, pk):
    profile = Profile.objects.get(user=request.user)
    productObj = get_object_or_404(MagazainProduct, id=pk)
    cart, created = CartedProduct.objects.get_or_create(user=profile, product=productObj)
    if True:
        corsina,created = Corsina.objects.get_or_create(user=profile)
        corsina.items.add(cart)
    # corsina,created = Corsina.objects.get_or_create(user=profile)
    # corsina.items.add(productObj)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def corsina_view(request):
    brands = Svoistva.objects.all()[:6]
    prices = []
    profile = Profile.objects.get(user=request.user)
    corsina = Corsina.objects.get(user=profile)
    categories = MainCategory.objects.all()[:8]

    products = corsina.items.all().count()
    full_price = 0
    if True:
        for i in corsina.items.all():
            prices.append(i.count * i.product.price)
        full_price = sum(prices)
        corsina.total_price = full_price
        corsina.save()



    return render(request, 'corsina.html', {'brands' : brands,'corsina' : corsina, 'categories' : categories, 'products' : products,'brands' : brands})

def remove_from_corsina(request, pk):
    productObj = get_object_or_404(CartedProduct, id=pk)
    profile = Profile.objects.get(user=request.user)
    corsina,created = Corsina.objects.get_or_create(user=profile)
    corsina.items.remove(productObj)
    productObj.delete()
    return redirect('corsina')

def add_quantite(request, pk):
    productObj = get_object_or_404(CartedProduct, id=pk)
    productObj.count += 1
    productObj.save()
    return redirect('corsina')

def minus_quantite(request, pk):
    productObj = get_object_or_404(CartedProduct, id=pk)
    productObj.count -= 1
    productObj.save()
    return redirect('corsina')

# For Brand


def brand_detail(request, slug):
    brands = Svoistva.objects.all()[:6]
    categories = MainCategory.objects.all()[:8]
    brand = get_object_or_404(Brand, slug=slug)
    brand_products = Product.objects.filter(brand=brand)
    products=0
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()

    return render(request, 'brand_detail.html', {'brand' : brand, 'brand_products' : brand_products, 'products' : products,
                                                'brands' : brands,
                                                'categories' : categories})


def show_unaviable_user(request, slug):
    categories = MainCategory.objects.all()[:8]
    brands = Brand.objects.all()[:6]
    brand = get_object_or_404(Brand, slug=slug)
    users = Profile.objects.filter(brand_member=brand)
    return render(request, 'admin_page.html', {'brand' : brand, 'users' : users,'brands' : brands, 'categories' : categories})


def make_aviable_user(request, pk):
    group = Group.objects.get(id=1)
    user = Profile.objects.get(id=pk)
    user.status = True
    # user.user.groups.add(group)
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def make_unaviable_user(request, pk):
    group = Group.objects.get(id=1)
    user = Profile.objects.get(id=pk)
    user.status = False
    # user.user.groups.remove(group)
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def show_unaviable_product(request, slug):
    categories = MainCategory.objects.all()[:8]
    brands = Svoistva.objects.all()[:6]
    brand = get_object_or_404(Brand, slug=slug)
    product = Product.objects.filter(brand=brand)
    return render(request, 'aviable_product.html', {'brand' : brand, 'product' : product,'brands' : brands, 'categories' : categories})

def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = UpdateProductForm(request.POST or None , request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('homepage')
    return render(request, 'update_product.html', {'form' : form})

def make_aviable_product(request, pk):
    product = Product.objects.get(id=pk)
    product.is_aviabale = True
    product.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def make_unaviable_product(request, pk):
    product = Product.objects.get(id=pk)
    product.is_aviabale = False
    product.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def become_member(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    profile = Profile.objects.get(user=request.user)
    profile.brand_member = brand
    profile.save()
    return redirect('homepage')


def admin_make_aviable_user(request, pk):
    group = Group.objects.get(id=1)
    user = Profile.objects.get(id=pk)
    user.is_brand_admin = True
    # user.user.groups.add(group)
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def admin_make_unaviable_user(request, pk):
    group = Group.objects.get(id=1)
    user = Profile.objects.get(id=pk)
    user.is_brand_admin = False
    # user.user.groups.remove(group)
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def brand_products(request, slug):
    brands = Svoistva.objects.all()[:6]
    brand_title = Brand.objects.get(slug = slug)
    categories = MainCategory.objects.all()[:8]
    # f = ProductSearch(request.GET, queryset=Product.objects.filter(is_aviabale=True, category__slug=slug))
    f = ProductFilter(request.GET, queryset=Product.objects.filter(brand__slug=slug, is_aviabale=True))

    products=0
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()
    return render(request, 'brand_products.html', {'filter' : f,'categories' : categories, 'products' : products, 'brand_title': brand_title,'brands' : brands})




# History
def add_to_history(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        productObj = get_object_or_404(corsina.items.get(id=pk))
    history, created = models.History.objects.get_or_create(user=profile)
    history.product.add(productObj)
    return HttpResponseRedirect('personal')







# Shop

def show_all_shop(request):
    shops = Shop.objects.all()
    return render(request, 'all_shops.html', {'shops' : shops})

def shop_detail(request, slug):
    brands = Svoistva.objects.all()[:6]
    categories = MainCategory.objects.all()[:8]
    shop = get_object_or_404(Shop, slug=slug)
    products=0
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()
    return render(request, 'shop_detail.html', {'shop' : shop,  'products' : products,
                                                'brands' : brands,
                                                'categories' : categories})

def delete_product(request, pk):
    product = MagazainProduct.objects.get(id=pk)   
    product.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
                   
def show_product_to_add(request, slug):
    brands = Svoistva.objects.all()[:6]
    categories = MainCategory.objects.all()[:8]
    shop = Shop.objects.get(slug=slug)
    a = MagazainProduct.objects.filter(shop=shop)
    productes = MagazainProduct.objects.filter(is_initial=True,  product__is_aviabale=True)
    products=0
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()
    return render(request, 'shop_show.html', {'productes' : productes, 'categories' : categories, 'products' : products,'brands' : brands})

def shop_add_product(request, pk):
    profile = Profile.objects.get(user=request.user)
    shops = Shop.objects.get(id=profile.shop_member.id)
    product = MagazainProduct.objects.get(id=pk)
    new_product = MagazainProduct.objects.create(product_id=product.product.id)
    new_product.shop = shops
    new_product.is_aviable = True
    new_product.is_initial = False
    new_product.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def show_shop_product(request, slug):
    brands = Svoistva.objects.all()[:6]
    categories = MainCategory.objects.all()[:8]
    shop = Shop.objects.get(slug=slug)
    productes = MagazainProduct.objects.filter(shop_id=shop)
    products=0
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        corsina = Corsina.objects.get(user=profile)
        products = corsina.items.all().count()
    return render(request, 'show_shops_product.html', {'productes' : productes, 'categories' : categories, 'products' : products,'brands' : brands})

def make_in_showable(request, pk):
    product = MagazainProduct.objects.get(id=pk)
    product.is_aviable = False
    product.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

def make_in_unshowable(request, pk):
    product = MagazainProduct.objects.get(id=pk)
    product.is_aviable = True
    product.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


def update_product_in_shop(request, pk):
    product = get_object_or_404(MagazainProduct, id=pk)
    form = UpdateForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('homepage')
    return render(request, 'update_shop_product.html', {'form' : form})


def create_product_shop(request):
    create_product = CreateShopProductForm()
    if request.method == 'POST':
        create_product = CreateShopProductForm(request.POST, request.FILES)
        if create_product.is_valid():
            create = create_product.save(commit=False)
            create.save()
        return redirect('homepage')
    return render(request, 'create_shop_product.html', {'form' : CreateShopProductForm})







def shop_show_unaviable_user(request, slug):
    categories = MainCategory.objects.all()[:8]
    brands = Brand.objects.all()[:6]
    shop = get_object_or_404(Shop, slug=slug)
    users = Profile.objects.filter(shop_member=shop)
    return render(request, 'admin_page.html', {'shop' : shop, 'users' : users,'brands' : brands, 'categories' : categories})


def shop_make_aviable_user(request, pk):
    group = Group.objects.get(id=1)
    user = Profile.objects.get(id=pk)
    user.shop_status = True
    # user.user.groups.add(group)
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def shop_make_unaviable_user(request, pk):
    group = Group.objects.get(id=1)
    user = Profile.objects.get(id=pk)
    user.shop_status = False
    # user.user.groups.remove(group)
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def become_member(request, slug):
    shop = get_object_or_404(Shop, slug=slug)
    profile = Profile.objects.get(user=request.user)
    profile.shop_member = shop
    profile.save()
    return redirect('homepage')