import base64

from django.core.files.base import ContentFile

from .format import decode_base64_and_save
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import StudentsForm
from django.http import HttpResponseRedirect
from .models import Students


@csrf_exempt
def register_student(request):
    submitted = False
    form = StudentsForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST.get('username')
            base64_data = request.POST.get('face')
            image_data = base64_data.split(',')[1]
            binary_data = base64.b64decode(image_data)
            with open(f'core/media/faces/{username}.png', 'wb') as file:
                file.write(binary_data)
            form.save()
            return render(request, 'registered.html')
    else:
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'form.html', {'submitted': submitted, 'form': form})


def mark_attendance(request):
    return render(request, 'attendance.html')


def home_page(request):
    return render(request, 'home.html')


def test_page(request):
    return render(request, 'home.html')
