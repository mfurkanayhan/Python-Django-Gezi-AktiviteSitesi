import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactFormu, ContactFormMessage
from product.models import Content, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Content.objects.all()[:4]
    category=Category.objects.all()
    eventcontents = Content.objects.all().order_by('?')[:6]
    #order_by ? kısmı idye göre random getirmek için..

    context={'setting':setting,
             'category': category,
             'page':'home',
             'sliderdata':sliderdata,
             'eventcontents': eventcontents
             }
    return render(request,'index.html', context)

def hakkimizda(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting':setting,
               'category': category
               }
    return render(request,'hakkimizda.html', context)

def referanslar(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting':setting,
               'category':category
               }
    return render(request,'referanslarimiz.html', context)


def iletisim(request):

    if request.method == 'POST': #form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage() # model ile bağlantı kur
            data.name = form.cleaned_data['name'] # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz ")
            return HttpResponseRedirect ('/iletisim')

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting':setting,'form':form,'category':category}
    return render(request,'iletisim.html', context)


def category_contents(request,id,slug):
    category = Category.objects.all()
    setting = Setting.objects.all()
    categorydata = Category.objects.get(pk=id)
    contents = Content.objects.filter(category_id=id)
    context = {'contents': contents,
               'category': category,
               'categorydata': categorydata,
               'setting': setting
               }
    return render(request,'contents.html',context)

def content_detail(request,id,slug):
    category = Category.objects.all()
    content = Content.objects.get(pk=id)
    images = Images.objects.filter(content_id=id)
    comments = Comment.objects.filter(content_id=id,status='True')
    context = {'content': content,
               'category': category,
               'images': images,
               'comments': comments,
               #'setting': setting
               }
    return render(request,'content_detail.html',context)

def content_search(request):
    if request.method == 'POST': # Check form post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()

            query = form.cleaned_data['query'] # Get form data
            catid = form.cleaned_data['catid'] #Get form data
            # return HttpResponse(catid
            if catid == 0:
                contents = Content.objects.filter(title__icontains=query)  # Select * from content where title like %query%
            else:
                contents = Content.objects.filter(title__icontains=query, category_id=catid)

            # return HttpResponse(contents)
            context = {'contents':contents,
                       'category':category,
                       }
            return render(request,'contents_search.html', context)
    return HttpResponseRedirect('/')

def content_search_auto(request):

    if request.is_ajax():
        q = request.GET.get('term', '')
        content = Content.objects.filter(title__icontains=q)
        results = []
        for rs in content:
            content_json = {}
            content_json = rs.title
            results.append(content_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Oturum Açma Hatası ! Kullanıcı adı veya şifre yanlış ")
            return HttpResponseRedirect ('/login')

    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html', context)




