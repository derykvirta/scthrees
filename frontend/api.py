from django.shortcuts import render
from django.http import HttpResponse

def stats(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')