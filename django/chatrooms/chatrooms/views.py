from django.http import HttpResponse

def homepage(request):
    return HttpResponse("Welcome to my homepage")

def about(request):
    return HttpResponse("This is the about page")