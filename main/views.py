from django.shortcuts import render


# Create your views here.
def index(req):
    return render(req, 'main/index.html')


def resume(req):
    return render(req, 'main/resume.html')
