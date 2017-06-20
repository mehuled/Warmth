from django.http import HttpResponse
from django.shortcuts import render
from warmth.models import Category, Page
from warmth.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



def index(request) :
    category_list =  Category.objects.order_by('-likes')
    pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories':category_list,
                    'pages': pages_list}
    return render(request,'warmth/index.html',context_dict)


def about(request) :
    context_dict = {'somemessage' : "I am a bold font About thing"}
    return render(request,'warmth/about.html',context_dict)

def exercise(request) :
    context_dict = {'m1' : 'This is message one houston',
                    'm2' : 'This is message second houston'}
    return render(request,'warmth/exercise.html',context_dict)

def category(request,category_name_slug) :
    context_dict = {}


    try :
        category = Category.objects.get(slug = category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist :
        pass

    return render(request,'warmth/category.html',context_dict)

@login_required
def add_category(request) :
    if request.method == 'POST' :
        form = CategoryForm(request.POST)

        if form.is_valid() :
            cat = form.save(commit=True)
            print cat,cat.slug
            return index(request)
        else :
            print form.errors
    else :
        form = CategoryForm()

    return render(request,'warmth/add_category.html',{'form':form, 'message':"My message!"})

@login_required
def add_page(request,category_name_slug) :

    try :
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist :
        cat = None

    if request.method == 'POST' :
        form = PageForm(request.POST)

        if form.is_valid() :

            if cat :
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request,category_name_slug)
        else :
            print form.errors
    else :
        form = PageForm()

    context_dict = {'form':form, 'category':cat, 'category_name_slug' : category_name_slug}

    return render(request,'warmth/add_page.html',context_dict)

def register(request) :

    registered = False

    if request.method == 'POST' :
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() :

            user = user_form.save()
            user.set_password(user.password)
            user.save()


            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES :
                profile.picture = request.FILES['picture']

            profile.save()
            registered =True

        else :
            print user_form.errors, profile_form.errors
    else :
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form,
                    'profile_form' : profile_form,
                    'registered' : registered,}
    return render(request,'warmth/register.html',context_dict)

def user_login(request) :
    if request.method == 'POST' :

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user :

            if user.is_active :
                login(request,user)

                return HttpResponseRedirect('/warmth/')
            else :
                return HttpResponse("Your warmth account is disabled")

        else :

            print "Invalid login details {0} : {1} ".format(username,password)
            return HttpResponse("Invalid login details supplied")

    else :

        return render(request,'warmth/login.html',{})


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/warmth/')

@login_required
def restricted(request) :
    return render(request,'warmth/restricted.html',{'message':"Since you are logged in you can see this page!"})
