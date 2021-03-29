from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import Services, TypeOfWork


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'counter/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('services')


class RegisterPage(FormView):
    template_name = 'counter/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('services')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('services')
        return super(RegisterPage, self).get(*args, **kwargs)


class ServicesList(LoginRequiredMixin, ListView):
    model = Services
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = context['services'].filter(user=self.request.user)
        return context


class ServicesDetail(LoginRequiredMixin, DetailView):
    model = Services
    context_object_name = 'service'
    template_name = 'counter/service.html'


class ServicesCreate(LoginRequiredMixin, CreateView):
    model = Services
    fields = ['price', 'service']
    success_url = reverse_lazy('services')

    def get_context_data(self, **kwargs):
        context = super(ServicesCreate, self).get_context_data(**kwargs)
        username = self.request.user
        context['form'].fields['service'].queryset = TypeOfWork.objects.all().filter(user__username=username)
        return context

    def form_valid(self, form):
        username = self.request.user
        form.instance.user = username
        form.instance.sum_for_worker = percent_sum(self.request)
        return super(ServicesCreate, self).form_valid(form)


class ServicesUpdate(LoginRequiredMixin, UpdateView):
    model = Services
    fields = ['price', 'service']
    success_url = reverse_lazy('services')

    def get_context_data(self, **kwargs):
        context = super(ServicesUpdate, self).get_context_data(**kwargs)
        username = self.request.user
        context['form'].fields['service'].queryset = TypeOfWork.objects.all().filter(user__username=username)
        return context

    def form_valid(self, form):
        username = self.request.user
        form.instance.user = username
        form.instance.sum_for_worker = percent_sum(self.request)
        return super(ServicesUpdate, self).form_valid(form)


class ServicesDelete(LoginRequiredMixin, DeleteView):
    model = Services
    context_object_name = 'service'
    template_name = 'counter/services_delete.html'
    success_url = reverse_lazy('services')


class TypeOfWorkList(ListView):
    model = TypeOfWork
    context_object_name = 'typeofwork'
    template_name = 'counter/typeofwork.html'

    def get_context_data(self, **kwargs):
        context = super(TypeOfWorkList, self).get_context_data(**kwargs)
        context['typeofwork'] = context['typeofwork'].filter(user=self.request.user)
        return context


class TypeOfWorkDetail(LoginRequiredMixin, DetailView):
    model = TypeOfWork
    context_object_name = 'work'
    template_name = 'counter/work_detail.html'


class TypeOfWorkCreate(LoginRequiredMixin, CreateView):
    model = TypeOfWork
    fields = ['title', 'fix_percent']
    success_url = reverse_lazy('typeofwork')

    def form_valid(self, form):
        username = self.request.user
        form.instance.user = username
        return super(TypeOfWorkCreate, self).form_valid(form)


class TypeOfWorkUpdate(LoginRequiredMixin, UpdateView):
    model = TypeOfWork
    fields = ['title', 'fix_percent']
    success_url = reverse_lazy('typeofwork')


class TypeOfWorkDelete(LoginRequiredMixin, DeleteView):
    model = TypeOfWork
    context_object_name = 'work_delete'
    template_name = 'counter/work_delete.html'
    success_url = reverse_lazy('typeofwork')


def percent_sum(request):
    typeser = TypeOfWork.objects.get(pk=request.POST['service'])
    percent = typeser.fix_percent
    sum_for_service = request.POST['price']
    end_sum = int(sum_for_service) / 100 * percent
    return end_sum
