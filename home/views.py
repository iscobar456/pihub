from django.shortcuts import render
from django.views import View

# Create your views here.

def homepage(request):

    context = {

    }
    return render(request, "index.html", context)

class Login(View):
    def get():
        print("it's a GET request")
    
    def post():
        print("it's a POST request")
