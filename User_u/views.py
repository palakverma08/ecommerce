from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms  import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate , login , logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import  unauthenticated_user,allowed_users,admin_only
from django.views.decorators.csrf import csrf_protect

# Create your views here.

from .models import*
from .forms import OrderForm ,CreateUserForm,CustomerForm
from .filters import OrderFilter

@unauthenticated_user
def registerPage(request):
    #if request.user.is_authenticated:
     #   return redirect('home')
  #  else:
      form = CreateUserForm()
      if request.method=='POST':
          form = CreateUserForm(request.POST)
          if form.is_valid():
             user= form.save()
             username =form.cleaned_data.get('username')

             group = Group.objects.get(name='customer')
             user.groups.add(group)
             Customer.objects.create(
                 user=user,
                 name=user.username,
                 )
             messages.success(request,'Account Created, Welcome!'+username)

             return redirect('login')

      context={'form':form}
      return render(request,'user/register.html',context)


@unauthenticated_user
def loginPage(request):
    #if request.user.is_authenticated:
   #     return redirect('home')
   # else:
      if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username ,password =password)
        
        if user is not None:
            login(request , user)
            return redirect('/')
        else:
            messages.info(request,'Username OR password incorrect')
           

            
      context={}
      return render(request,'user/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders= Order.objects.all()
    customers = Customer.objects.all()

    total_customers= customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = { 'orders':orders,'customers':customers ,
               'total_orders':total_orders,'delivered':delivered
               ,'pending':pending}
    return render(request,'user/dashboard.html' ,context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:',orders)

    context ={'orders':orders ,
               'total_orders':total_orders,'delivered':delivered
               ,'pending':pending}
    return render(request,'user/user.html' ,context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method =='POST':
        form =CustomerForm(request.POST,request.FILES,instance=customer)

        if form.is_valid():
           form.save()
           
    context ={'form':form}
    return render(request,'user/accounts_settings.html' ,context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    product=Product.objects.all()
    return render(request,'user/product.html' ,{'product':product})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request ,pk_test):
    customer= Customer.objects.get(id=pk_test)

    orders= customer.order_set.all()
    order_count =orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders =myFilter.qs

    context = {'customer':customer ,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'user/customer.html',context)

def main(request):
  return render(request,'user/main.html')

def navbar(request):
   return render(request,'user/navbar.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset = Order.objects.none(),instance=customer)

    if request.method == 'POST':
       # print('Printing Post:',request.POST)
      # form = OrderForm(request.POST)
     formset = OrderFormSet(request.POST,instance=customer) 
    if formset.is_valid():
           formset.save()
           return redirect('/')

    context = {'formset' : formset}
   # context = {}
    return render(request, 'user/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
     order = Order.objects.get(id=pk)
     form = OrderForm(instance=order)

     if request.method == 'POST':
       # print('Printing Post:',request.POST)
       form = OrderForm(request.POST,instance=order)
       if form.is_valid():
           form.save()
           return redirect('/')

     context = {'form' : form}
     return render(request, 'user/order_form.html',context)
 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
     order = Order.objects.get(id=pk)
     if request.method =='POST':
        order.delete()
        return redirect('/')
     context ={'item':order}
     return render(request,'user/delete.html',context)