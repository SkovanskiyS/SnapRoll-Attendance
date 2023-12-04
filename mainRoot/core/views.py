import base64

import pandas as pd
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from .camera import FaceRecognition
from .forms import StudentsForm
from .models import Students
from .serializers import StudentsSerializer

fr = FaceRecognition()


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


@xframe_options_exempt
def frame1(request):
    return render(request, 'frame1.html')


@xframe_options_exempt
def frame2(request):
    fr.stop_flag = True
    user_data = []
    for user in fr.attended_students:
        user_data.append(get_object_or_404(Students, username=user))
    serializer = StudentsSerializer(user_data, many=True).data
    serializer = [{k: v for k, v in user.items() if k != 'password'} for user in serializer]
    request.session['user_info'] = serializer

    return render(request, 'frame2.html', context={'students_data': user_data})


def mark_attendance(request):
    if request.method == 'POST':
        # return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')
        fr.stop_flag = False
        data = request.POST
        data = dict(data)
        del data['csrfmiddlewaretoken']
        request.session['attendance_header'] = data
        return render(request, 'mark_attendance.html', context={'context': data})
    return render(request, 'attendance.html')


def facecam_feed(request):
    return StreamingHttpResponse(fr.run_recognition(), content_type='multipart/x-mixed-replace; boundary=frame')


def home_page(request):
    return render(request, 'home.html')


def test_page(request):
    return render(request, 'home.html')


def get_names(request):
    student_data = request.session.get('user_info', [])
    header_data = request.session.get('attendance_header', [])

    students_df = pd.DataFrame(student_data)

    header_df = pd.DataFrame({
        'faculty': [header_data.get('faculty')[0]],
        'semester': [header_data.get('semester')[0]],
        'section': [header_data.get('section')[0]],
        'room number': [header_data.get('room number')[0]],
        'date': [header_data.get('date')[0]]
    })

    final_df = pd.concat([header_df, students_df], ignore_index=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"{header_data.get('faculty')[0]} {header_data.get('date')[0]}"
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'

    final_df.to_excel(response, index=False)

    return response

