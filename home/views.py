from django.shortcuts import render
from django.views import View

# Create your views here.

def homepage(request):

    context = {

    }
    return render(request, "index.html", context)

class Login(View):
    def get(self, request, *args, **kwargs):

        context = {
            
        }
        return render(request, "login.html", context)
    
    def post():
        print("it's a POST request")
