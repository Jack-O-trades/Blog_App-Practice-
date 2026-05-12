from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to My Blog Front Page</h1>')
