from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

def base(request):
    return render(request, 'testboard/test.html', {
    })

