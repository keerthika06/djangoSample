from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from article.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required



# Create your views here.

def home(request):
    queryset = Article.objects.all()
    context = { 'articles':queryset}
   

    return render(request, "base.html",context)

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
                return redirect('/author-page/')
            elif user.is_publisher:
                return redirect('/publisher-article')
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
    return render(request, 'addUser.html' )





@login_required
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
            articleDescription = articleDescription,
            user = request.user
        )
        #return redirect('/add-article/')
    #queryset= Article.objects.all()
    #queryset= Article.objects.filter(user = request.user)


    #if request.GET.get('search'):
       # queryset = queryset.filter(recepie_name__icontains = request.GET.get('search'))
       # print(request.GET.get('search'))
    # for q in queryset:
    #     if q.isreviewd is False:
    #         print(q)
    
    author = request.user
    print(author)
    #context = {'articles': queryset}
    return render(request, "addArticle.html")

    #queryset= Article.objects.all()
    #context = {'recepies': queryset}
    





    #return render(request, "addArticle.html")

def authorPage(request):
    
    queryset = Article.objects.all()
    context = { 'articles':queryset}
   

    return render(request, "authorpage.html",context)


def viewUsers(request):
    queryset= User.objects.all()
    print(queryset)
    context = {'users': queryset}

    return render(request, "viewUsers.html",context)

@login_required
def showArticletoauthor(request):
    author = request.user
    print("hiii",author)
    queryset= Article.objects.filter(user = author)
    #queryset = Article.objects.all()
    print(queryset)
    
    context = { 'articles':queryset}
    
    return render(request, "showArticle.html",context)



def showArticle(request):
    queryset = Article.objects.all()
    context = { 'articles':queryset}
    return render(request, "showArticle.html",context)


def draftArticle(request):
    #queryset= Article.objects.filter(user = author)
    author = request.user
    queryset = Article.objects.filter(Q(articlestatus ='draft') & Q(user = author))
    context = { 'articles':queryset}
    
    return render(request, 'showArticle.html',context)

def update_article(request, id):
    queryset = Article.objects.get(id = id)
    if request.method == "POST":
        data = request.POST
        articleTitle = data.get('articleTitle')
        articleSubTitle = data.get('articleSubTitle')
        articleThumbnail = request.FILES.get('articleThumbnail')
        articleDescription = data.get('articleDescription')

        queryset.articleTitle = articleTitle
        queryset.articleSubTitle = articleSubTitle
        queryset.articleDescription = articleDescription

        if articleThumbnail:
            queryset.articleThumbnail = articleThumbnail
        queryset.save()
        return redirect('/add-article/')
    context = {'article': queryset}
    return render(request , 'updateArticle.html',context)
def publisherArticle(request):
  
  queryset = Article.objects.filter()
  context = { 'articles':queryset}
  return render(request, 'publisherindex.html',context)


# def individualarticle(request,id):
#     #queryset = Article.objects.get(id = id)
#     if request.method == 'POST':
#         aorr = request.POST.get('aorr')
#         articles = Article.objects.get(pk=id)
#         articles.status = aorr
#         articles.save()


        #if aorr == "Accept":
           # queryset.articlestatus = "Published"
         #   messages.info(request, 'Article published succesfully')
       # else:
        #    queryset.articlestatus = "Rejected"
       #     messages.info(request, 'Article rejected')
      #  queryset.save()
        # return redirect('publisher-article')
    #context = { 'articles':queryset }
    # return render(request ,'indivialarticle.html')

def individualarticle(request, pk):

    if request.method == 'POST':
        status = request.POST.get('status')
        articles = Article.objects.get(pk=pk)
        articles.articlestatus = status
        articles.save()
        return redirect('publisherArticle')
    articles = Article.objects.get(pk=pk)
    return render(request, 'indivialarticle.html',{"articles":articles})




def publisherAccept(request,id):
    print("hiii")
    queryset = Article.objects.get(id = id)
    context = { 'articles':queryset}

   

    return render(request ,'indivialarticle.html',context)
    
def delete_article(request,id):
    queryset = Article.objects.get(id = id)
    queryset.delete()

    return redirect('/show-article/')
def logout_page(request):
    logout(request)

    return redirect('/login/')

