from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage
from product.models import Content, Category


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
