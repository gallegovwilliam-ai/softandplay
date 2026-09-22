from django.shortcuts import render, HttpResponse, redirect
from django.urls import  reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.db.models.query import QuerySet
from django.db.models import Avg, Count, Q
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404
from .models import Cliente
from .forms import ClienteForm

class ClienteCreate(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'add_cliente.html'
    success_url = reverse_lazy('list-cliente')
    def post(self,*args,**kwargs):
        if not self.request.user.is_authenticated:
            raise Http404
        Cliente.objects.create(
            user_id=self.request.user.pk,
            nombre=self.request.POST.get('nombre',''),
            apellido=self.request.POST.get('apellido',''),
            dni=self.request.POST.get('dni',''),
            direccion=self.request.POST.get('direccion',''),
            telefono=self.request.POST.get('telefono',''),
            email=self.request.POST.get('email',''),
            )
        return redirect(reverse_lazy('list-cliente'))
ClienteCreate = ClienteCreate.as_view()

class ClienteUpdate(UpdateView):
    model = Cliente
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(user=self.request.user)
    form_class = ClienteForm
    template_name = 'update_cliente.html'
    success_url = reverse_lazy('list-cliente')
ClienteUpdate = ClienteUpdate.as_view()



class ClienteList(ListView):
    model = Cliente
    template_name = 'list_cliente.html'
    def get_queryset(self,*args,**kwargs):
        qs = Cliente.objects.filter(active=True)
        if self.request.user.is_superuser:
            return qs
        return qs.filter(user=self.request.user)
ClienteList = ClienteList.as_view()


@login_required
def VerificarCliente(request):
    try:
        c = Cliente.objects.get(pk=request.GET['cedula'])
    except ObjectDoesNotExist:
        return HttpResponse('NoExiste')
    if not request.user.is_superuser and c.user_id != request.user.pk:
        raise Http404
    return JsonResponse({'nombre':c.nombre,'telefono':c.telefono})

def ClienteDelete(request,pk):
    if request.method != 'POST':
        return HttpResponse(status=405)
    qs = Cliente.objects.filter(pk=pk)
    if not request.user.is_superuser:
        qs = qs.filter(user=request.user)
    if not qs.exists():
        raise Http404
    qs.update(active=False)
    return redirect(reverse_lazy('cliente-list'))