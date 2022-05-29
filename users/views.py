from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.contrib.auth import login, authenticate 
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm 

from .models import *
from .forms import *
from items.models import *

def is_admin(user):
    return user.groups.filter(name='is_admin_brand').exists()

def can_add(user):
    return user.groups.filter(name='is_member').exists()

def lichnyi_cabinet(request):
    brands = Svoistva.objects.all()[:6]
    profile = Profile.objects.get(user=request.user)
    history = History.objects.get(user=profile)
    categories = MainCategory.objects.all()[:8]
    return render(request, 'personal_cabinet.html', {'profile' : profile, 'history' : history,'categories' : categories,'brands' : brands})

def personal_cabinet(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        productObj = Corsina.objects.get(user=profile)
        if productObj.items.count() == 0:
            None
        if productObj.items.count() == 1:
            # for i in productObj.items.all().first():
            i = productObj.items.first()
            historyObj = HistoryProduct.objects.create(name=i.product.product.name, price = i.product.price,
                                        count = i.count, samovyzov= i.samovyzov)
            history = History.objects.get(user=profile)
            history.product.add(historyObj)
            history.save()
            productObj.items.remove(*productObj.items.all())
            productObj.save()
        if productObj.items.count() == 2:
            j = productObj.items.all()
            first = j[0]
            historyObj1 = HistoryProduct.objects.create(name=first.product.product.name, price =first.product.price,
                                        count = first.count, samovyzov= first.samovyzov)
            second = j[1]
            historyObj2 = HistoryProduct.objects.create(name=second.product.product.name, price =second.product.price,
                                        count = second.count, samovyzov= second.samovyzov)
            history = History.objects.get(user=profile)
            history.product.add(historyObj1)
            history.product.add(historyObj2)
            history.save()
            productObj.items.remove(*productObj.items.all())
            productObj.save()
        if productObj.items.count() == 3:
            j = productObj.items.all()
            first = j[0]
            historyObj1 = HistoryProduct.objects.create(name=first.product.product.name, price =first.product.price,
                                        count = first.count, samovyzov= first.samovyzov)
            second = j[1]
            historyObj2 = HistoryProduct.objects.create(name=second.product.product.name, price =second.product.price,
                                        count = second.count, samovyzov= second.samovyzov)
            third = j[2]
            historyObj3 = HistoryProduct.objects.create(name=third.product.product.name, price =third.product.price,
                                        count = third.count, samovyzov= third.samovyzov)
            history = History.objects.get(user=profile)
            history.product.add(historyObj1)
            history.product.add(historyObj2)
            history.product.add(historyObj3) 
            history.save()
            productObj.items.remove(*productObj.items.all())
            productObj.save()
        if productObj.items.count() == 4:
            j = productObj.items.all()
            first = j[0]
            historyObj1 = HistoryProduct.objects.create(name=first.product.product.name, price =first.product.price,
                                        count = first.count, samovyzov= first.samovyzov)
            second = j[1]
            historyObj2 = HistoryProduct.objects.create(name=second.product.product.name, price =second.product.price,
                                        count = second.count, samovyzov= second.samovyzov)
            third = j[2]
            historyObj3 = HistoryProduct.objects.create(name=third.product.product.name, price =third.product.price,
                                        count = third.count, samovyzov= third.samovyzov)
            fourth = j[3]
            historyObj4 = HistoryProduct.objects.create(name=fourth.product.product.name, price =fourth.product.price,
                                        count = fourth.count, samovyzov= fourth.samovyzov)
            history = History.objects.get(user=profile)
            history.product.add(historyObj1)
            history.product.add(historyObj2)
            history.product.add(historyObj3)
            history.product.add(historyObj4)
            history.save()
            productObj.items.remove(*productObj.items.all())
            productObj.save()
    return HttpResponseRedirect('cabinet')
       
def clear_history(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        history = History.objects.get(user=profile)
        history.product.remove(*history.product.all())
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def signup_view(request):
    userForm=UserForm()
    profileForm=ProfileForm()
    mydict={'userForm':userForm,'profileForm':profileForm}
    if request.method=='POST':
        userForm=UserForm(request.POST)
        profileForm=ProfileForm(request.POST,request.FILES)
        if userForm.is_valid() and profileForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            profile=profileForm.save(commit=False)
            profile.user=user
            profile.save()
        return HttpResponseRedirect('/')
    return render(request,'register.html',context=mydict)

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return HttpResponseRedirect('shop/')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def createcommentproduct(request, pk):
    comment = CommetProductForm()
    if request.method == 'POST':
        comment = CommetProductForm(request.POST)
        if comment.is_valid():
            comments = comment.save(commit=False)
            try:
                profile = Profile.objects.get(user=request.user)
                comments.user = profile
                product = Product.objects.get(id=pk)
                comments.product = product
            except:
                return 'Some error'
            comments.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))