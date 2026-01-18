from django.shortcuts import render

def login_page(request):
    return render(request,"login.html")

def register_page(request):
    return render(request,"register.html")

def search_page(request):
    return render(request,"search.html")
