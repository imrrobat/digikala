from django.shortcuts import render
def helloworld(request):
    return render(request, 'shop/templates/index.html')


