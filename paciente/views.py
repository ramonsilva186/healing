from django.shortcuts import render, redirect
from medico.models import DadosMedicos, Especialidades, DatasAbertas
from django.http import HttpResponse
from datetime import datetime
from .models import Consulta
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
def home(request):

    if request.method == 'GET':

        medico_filtrar = request.GET.get('medico')
        especialidade_filtrar = request.GET.getlist('especialidade')
        medicos = DadosMedicos.objects.all()

        if medico_filtrar:
            medicos = medicos.filter(nome__icontains=medico_filtrar)

        if especialidade_filtrar:
            medicos = medicos.filter(especialidade__in=especialidade_filtrar)

        especialidades = Especialidades.objects.all() 
        return render(request, 'home.html', {'medicos': medicos, 'especialidades': especialidades})

def escolher_horario(request, id_dados_medicos):
    if request.method == 'GET':
        medico = DadosMedicos.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)
        return render(request, 'escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas})

def agendar_horario(request, id_data_aberta):
    
    if request.method == 'GET':
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)
        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )
        horario_agendado.save()
        data_aberta.agendado = True
        data_aberta.save()
        messages.add_message(request, constants.SUCCESS, 'Agendado com sucesso')

        return redirect('/pacientes/minhas_consultas/')

    if request.method == 'POST':
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)
        data_aberta.agendado = True
        data_aberta.save()
        return HttpResponse('Agendado com sucesso')