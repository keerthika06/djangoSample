from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from article.models import User

# Create your views here.

def home(request):
   

    return render(request, "base.html")

def articles(request):

 

  return render(request, 'base.html')

def login_page(request):
   if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("user",username)

        print(User.objects.values_list('username', flat=True))
        if not User.objects.filter(username = username).exists():
            print("hiiiiiiiiii",username)
            messages.error(request,'Invalid Username')
            return redirect('/login/')
        user = authenticate(username = username, password = password)
    
        if user is None :
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request,user)
            if user.is_superuser:
          
                return redirect('/add-user/')
            elif user.is_author:
                return redirect('/addArticle')
            elif user.is_publisher:
                return redirect('/Publisher')
            else:
                messages.error(request, 'Try to login again.')
                return redirect('/login/')
   return render(request, "login.html")
   

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        role = request.POST.get('role')
        print("hiiiiiiii",role)
        user = User.objects.filter(username = username)
        if user.exists():
            messages.error(request,'Username already exist')
            return redirect('/add-user/')
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        if role == "Author":
            user.is_author = True
        else:
            user.is_publisher = True

            


#**********************
        user.save()

        messages.info(request, 'Account successfully created')

        return redirect('/add-user/')
    return render(request, 'addUser.html')
def add_article(request):
    if request.method == "POST":
        data = request.POST
        articleTitle = data.get('articleTitle')
        articleSubTitle = data.get('articleSubTitle')
        articleThumbnail = request.FILES.get('articleThumbnail')
        articleDescription = data.get('articleDescription')

        Article.objects.create(
            articleTitle = articleTitle,
            articleSubTitle = articleSubTitle,
            articleThumbnail = articleThumbnail,
            articleDescription = articleDescription
        )


    return render(request, "addArticle.html")

def showArticle(request):
    queryset = Article.objects.all()
    context = {'articles':queryset}
   

    return render(request, "showArticle.html",context)