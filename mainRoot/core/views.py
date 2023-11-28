from django.shortcuts import render


def home_page(request):
    return render(request, 'form.html')


def test_page(request):
    return render(request, 'test.html')
