from django.shortcuts import render
from medico.models import DadosMedicos

# Create your views here.
def home(request):

    if request.method == 'GET':
        medicos = DadosMedicos.objects.all()
        return render(request, 'home.html', {'medicos': medicos})