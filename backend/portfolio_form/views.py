from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def submitForm(request):
    if request.method == 'POST':
        
        return HttpResponse('Form submitted successfully!')
    else:
        return HttpResponse('Invalid request method.')
