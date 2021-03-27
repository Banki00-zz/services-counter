from django.shortcuts import render, redirect
from .forms import *
from .models import *


# Create your views here.
def index(request):

    services = AddService.objects.all().order_by('-date_add')[:5]
    form = AddServiceForm()

    if request.method == "POST":
        service = AddService()
        service.price = request.POST['price']
        service.sum_for_worker = sum_for_worker(request)
        service.service_id = request.POST['service']
        service.save()
        return redirect('/')

    context = {"services": services, "form": form}
    return render(request, "html/index.html", context)


def update_service(request, pk):

    service = AddService.objects.get(id=pk)
    form = AddServiceForm(instance=service)
    context = {'form': form}
    if request.method == 'POST':
        form = AddServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, "html/update_service.html", context)


def delete_service(request, pk):

    service = AddService.objects.get(id=pk)
    if request.method == "POST":
        service.delete()
        return redirect('/')

    return render(request, "html/delete_service.html")


def sum_for_worker(request):
    id_service = request.POST['service']
    type_service = TypeOfWork.objects.get(id=id_service)
    percent = type_service.fix_percent
    price = request.POST['price']
    sumforworker = int(price) / 100 * int(percent)
    return sumforworker