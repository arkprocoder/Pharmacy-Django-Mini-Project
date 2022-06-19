import re
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
# Create your views here.
from app.models import Contact,Medicines,ProductItems,MyOrders


def Home(request):
    mymed=Medicines.objects.all()
    myprod=ProductItems.objects.all()
    context={"mymed":mymed,"myprod":myprod}
    return render(request, "Home.html",context)


def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phon=request.POST.get("num")
        desc=request.POST.get("desc")
        query=Contact(name=name,email=email,phoneno=phon,desc=desc)
        query.save()
        messages.info(request,f"Thank You. Will Get back you soon {name}")

    return render(request, "contact.html")


def About(request):
    return render(request, "About.html")


def HandleSignup(request):
    # logic
    if request.method == "POST":

        uname = request.POST.get("username")
        email = request.POST.get("email")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        pass1 = request.POST.get("pass1")
        cpass = request.POST.get("pass2")
        # print(uname,email,fname,lname,pass1,cpass)

# check wheater user exists or not
        if(pass1 != cpass):
            messages.warning(request,"Password is'nt Matching")
            return redirect("/signup")

        try:
            if User.objects.get(username=email):
                messages.info(request,"Username is taken..")
                return redirect("/signup")
        except:
            pass

        myuser = User.objects.create_user(email, uname, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request,"Signup Success")
        return redirect("/login")

    return render(request, "signup.html")


def HandleLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        # print(email,pass1)
        myuser = authenticate(username=email, password=pass1)

        if myuser is not None:
            login(request, myuser)
            messages.info(request,"Login Successful")
            return redirect("/")

        else:
            messages.error(request,"Invalid Credentials")
            return redirect("/login")

    return render(request, "login.html")


def HandleLogout(request):
    logout(request)
    messages.warning(request,"Logout")
    return redirect("/login")


def medicines(request):
    mymed=Medicines.objects.all()
    context={"mymed":mymed}
    # print(context)
    return render(request,"medicines.html",context)


def products(request):
    myprod=ProductItems.objects.all()
    context={"myprod":myprod}
    # print(context)
    return render(request,"products.html",context)



def myorders(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login to place the Order....")
        return redirect("/login")
    mymed=Medicines.objects.all()
    myprod=ProductItems.objects.all()

    # i am writing a logic to get the user details orders
    current_user=request.user.username
    # print(current_user)
    # i am fetching the data from table MyOrders based on emailid
    items=MyOrders.objects.filter(email=current_user)
    print(items)
    context={"myprod":myprod,"mymed":mymed,"items":items}
    if request.method =="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        item=request.POST.get("items")
        quan=request.POST.get("quantity")
        address=request.POST.get("address")
        phone=request.POST.get("num")
        print(name,email,item,quan,address,phone)
        
        price=""
        for i in mymed:
            if item==i.medicine_name:
                price=i.medicine_price

            pass
        for i in myprod:
            if item==i.prod_name:
                price=i.prod_price

            pass

        newPrice=int(price)*int(quan)
        myquery=MyOrders(name=name,email=email,items=item,address=address,quantity=quan,price=newPrice,phone_num=phone)
        myquery.save()
        messages.info(request,f"Order is Successfull")
        return redirect("/orders")

    
    return render(request,"orders.html",context)


def search(request):
    query=request.GET["getdata"]
    print(query)
    allPostsMedicines=Medicines.objects.filter(medicine_name__icontains=query)
    allPostsProducts=ProductItems.objects.filter(prod_name__icontains=query)
    allPosts=allPostsMedicines.union(allPostsProducts)
    
    return render(request,"search.html",{"Med":allPostsMedicines,"Prod":allPostsProducts,"allItems":allPosts})



def deleteOrder(request,id):
    print(id)
    query=MyOrders.objects.get(id=id)
    query.delete()
    messages.success(request,"Order Cancelled Successfully..")
    return redirect("/orders")