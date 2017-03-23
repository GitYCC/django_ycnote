from django.shortcuts import render

from django.http import cookie
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import Http404
from Posts.models import Post

import pprint, re, datetime, logging

from django.core.cache import cache

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_loggin(request):
    return request.user!="AnonymousUser"

def record_ip(request):
    ip = get_client_ip(request)
    method = request.method
    path = request.get_full_path()
    agent = request.META.get('HTTP_USER_AGENT')
    user = request.user
    string = "{}|{}|{} {}|{}|:|".format(ip,user,method,path,agent)
    with open("login.log","a") as f:
        f.write(string)

def welcome(request):
    #l = filter(lambda x: x.startswith('HTTP_'),request.META.keys())
    #l = list(l)
    #print(l)
    #for i in l:
    #    print("{}, {}".format(i,str(request.META[i])))
    record_ip(request)
    if request.method == 'GET':
        return render(request,'welcome.html',{})


    elif request.method == 'POST':
        pass


def me(request):
    #l = filter(lambda x: x.startswith('HTTP_'),request.META.keys())
    #l = list(l)
    #print(l)
    #for i in l:
    #    print("{}, {}".format(i,str(request.META[i])))
    record_ip(request)
    if request.method == 'GET':
        return render(request,'me.html',{})


    elif request.method == 'POST':
        pass


    


def coding(request):
    record_ip(request)

    if request.method == 'GET':
        posts = cache.get('coding_posts')
        if not posts:
            logging.warning("recharge cache with 'coding'")
            posts = Post.objects.filter(kind__contains="Coding").filter(isPublic__exact=True)
            posts = posts.order_by('-post_time')
            cache.set("coding_posts",posts,1800)
           

        return render(request,'posts.html',
            {'posts':posts,'title':"Coding",
            'subtitle':"Mechine Learning | Algorithm | Python",
            'front_board_img':"/static/img/coding_front_board.jpg"
            })


    elif request.method == 'POST':
        pass

def reading(request):
    record_ip(request)
    if request.method == 'GET':
        posts = cache.get('reading_posts')
        if not posts:
            logging.warning("recharge cache with 'reading'")
            posts = Post.objects.filter(kind__contains="Reading").filter(isPublic__exact=True)
            posts = posts.order_by('-post_time')
            cache.set("reading_posts",posts,1800)

        return render(request,'posts.html',
            {'posts':posts,'title':"Reading",
            'subtitle':"Be a Scientist",
            'front_board_img':"/static/img/reading_front_board.jpg"
            })


    elif request.method == 'POST':
        pass

def living(request):
    record_ip(request)
    if request.method == 'GET':
        posts = cache.get('living_posts')
        if not posts:
            logging.warning("recharge cache with 'living'")
            posts = Post.objects.filter(kind__contains="Living").filter(isPublic__exact=True)
            posts = posts.order_by('-post_time')
            cache.get("living_posts",posts,1800)

        return render(request,'posts.html',
            {'posts':posts,'title':"Living",
            'subtitle':"My Life is Brilliant",
            'front_board_img':"/static/img/living_front_board.jpg"
            })


    elif request.method == 'POST':
        pass

def post(request,pk):
    record_ip(request)
    if request.method == 'GET':
        post = Post.objects.get(pk=pk)

        if not post.front_board:
            if post.kind == "Coding":
                post.front_board = "/static/img/coding_front_board.jpg"
            elif post.kind == "Reading":
                post.front_board = "/static/img/reading_front_board.jpg"
            elif post.kind == "Living":
                post.front_board = "/static/img/living_front_board.jpg"

        if not post:
            return Http404
        else:
            return render(request,'post.html',
                {'post':post})


    elif request.method == 'POST':
        pass


