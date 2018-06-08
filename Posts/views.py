from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from .forms import PostCreateForm
from .models import Post
from django.utils import timezone
from django.core.paginator import Paginator
from urllib.parse import urlparse, urlencode

num_post_per_page = 15

def redirectTo(url):
    return HttpResponseRedirect(reverse(url))

def _create_post(form, u):
    data = form.cleaned_data
    instance = Post.objects.create(user=u)

    instance.title = data['title']
    instance.price = data['price']
    instance.is_for_sale = data['is_for_sale']

    instance.rooms = data['rooms']
    instance.floor = data['floor']
    instance.address = data['address']

    instance.description = data['description']
    instance.city = data['city']

    instance.timestamp = timezone.now()

    instance.image_1 = data['image_1']
    instance.image_2 = data['image_2']
    instance.image_3 = data['image_3']

    instance.save()
    return instance

def create(request):
    c_user = request.user
    if not c_user.is_authenticated:
        return redirectTo('login:login')

    if request.method == 'GET':
        post_form = PostCreateForm()
        ctx = {
            'user': request.user,
            'f': post_form
        }
        return render(request, 'posts/create.html', context=ctx)
    else:
        post_form = PostCreateForm(request.POST, request.FILES)
        if post_form.is_valid():
            p = _create_post(post_form, c_user)
            return HttpResponseRedirect(reverse('post:detail', args=[p.id]))
        return HttpResponse('Error in form')

def posts(request):
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    p = Paginator(Post.objects.all(), num_post_per_page)

    if page <= 0 or page > p.num_pages:
        page = 1

    posts = p.page(page)
    prev = []
    next = []
    for i in range(1, 3):
        if posts.number-i > 0: prev = [posts.number-i] + prev
    for i in range(1, 3):
        if posts.number+1 < p.num_pages: next.append(posts.number+i)

    return render(request, 'posts/posts.html', {'posts': posts, 'user': request.user, 'next': next, 'prev': prev})

def detail_post(request, p_id):
    post = get_object_or_404(Post, id = p_id)
    ctx = {
        'post': post,
        'user': request.user
    }
    return render(request, 'posts/view.html', context=ctx)

def search(request):
    q = request.GET.get('q', '')
    city = request.GET.get('city', '')
    tpy = request.GET.get('type', '')
    minPrice = request.GET.get('minPrice', '0')
    maxPrice = request.GET.get('maxPrice', '0')
    room = request.GET.get('rooms', '0')

    obj = Post.objects.all()
    if city:
        nobj = []
        city = city.lower()
        for o in obj:
            if city in o.city.lower() or o.city.lower() in city:
                nobj.append(o)
        obj = nobj
    if tpy:
        b = True if tpy.lower() in 'sale' else False
        nobj = []
        for o in obj:
            if o.is_for_sale == b:
                nobj.append(o)
        obj = nobj

    if room:
        try:
            n = int(room)
        except:
            n = -1
        if n != -1:
            nobj = []
            for o in obj:
                if o.rooms == n:
                    nobj.append(o)
            obj = nobj
    if minPrice:
        try:
            n = int(minPrice)
        except:
            n = -1
        nobj = []
        for o in obj:
            if o.price >= n:
                nobj.append(o)
        obj = nobj

    if maxPrice:
        try:
            n = int(maxPrice)
        except:
            n = 1213333333333333333333333333333333333333333332333333333
        nobj = []
        for o in obj:
            if o.price <= n:
                nobj.append(o)
        obj = nobj

    if q:
        nobj = []
        for o in nobj:
            if q in o.title or q in o.address or q in o.description:
                nobj.append(o)
        obj = nobj

    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    p = Paginator(obj, num_post_per_page)

    if page <= 0 or page > p.num_pages:
        page = 1

    posts = p.page(page)
    prev = []
    next = []
    for i in range(1, 3):
        if posts.number-i > 0: prev = [posts.number-i] + prev
    for i in range(1, 3):
        if posts.number+1 < p.num_pages: next.append(posts.number+i)

    url = urlencode({'q': q, 'city':city, 'type': tpy, 'minPrice': minPrice, 'maxPrice': maxPrice, 'rooms': room})
    url = 'post/search/?'+url
    print(url)

    return render(request, 'posts/search.html', {'posts': posts, 'user': request.user, 'next': next, 'prev': prev, 'cu': url})