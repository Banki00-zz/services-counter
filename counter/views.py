import datetime, re
from django.db.models import Sum
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
    """Форма авторизации с переадресацией"""
    template_name = 'counter/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('services')


class RegisterPage(FormView):
    """Форма регистрации"""
    template_name = 'counter/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('services')

    def form_valid(self, form):
        """Автоматический вход после регистрации"""
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        """Если пользователь зареган, редирект на глав. страницу"""
        if self.request.user.is_authenticated:
            return redirect('services')
        return super(RegisterPage, self).get(*args, **kwargs)


class ServicesList(LoginRequiredMixin, ListView):
    """Список оказанных услуг"""
    model = Services
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        """Фильтруем услуги по пользователю и подсчет зп за выбраный месяц"""
        context = super().get_context_data(**kwargs)
        month = datetime.date.today().month
        context['services'] = context['services'].filter(user=self.request.user, date_add__month=month).order_by('-date_add')[:5]
        context['count'] = Services.objects.filter(user=self.request.user, date_add__month=month).aggregate(Sum('sum_for_worker'))
        search_input = self.request.GET.get('search-area')

        if search_input:
            value = re.split(r'-', search_input)[1]
            context['services'] = Services.objects.filter(user=self.request.user, date_add__month=value).order_by('-date_add')[:5]
            context['count'] = Services.objects.filter(user=self.request.user, date_add__month=value).aggregate(Sum('sum_for_worker'))
            context['search_input'] = search_input
            context['word'] = 'месяц'
            return context
        return context


class AllServicesList(LoginRequiredMixin, ListView):
    model = Services
    context_object_name = 'all_services'
    template_name = 'counter/all_services_list.html'

    def get_context_data(self, **kwargs):
        """Фильтруем услуги по пользователю и подсчет зп за выбраный месяц"""
        context = super().get_context_data(**kwargs)
        value = datetime.date.today().month
        search_input = self.request.GET.get('search-area')
        day_search_input = self.request.GET.get('day-search-area')
        context['word'] = 'месяц'

        if search_input:
            value = re.split(r'-', search_input)[1]
            context['search_input'] = search_input
            context['word'] = 'месяц'

        elif day_search_input:
            value = re.split(r'-', day_search_input)[2]
            context['all_services'] = context['all_services'].filter(user=self.request.user,
                                                                     date_add__day=value).order_by('-date_add')
            context['count'] = Services.objects.filter(user=self.request.user, date_add__day=value).aggregate(
                Sum('sum_for_worker'))
            context['day_search_input'] = day_search_input
            context['word'] = 'день'
            return context
        context['all_services'] = context['all_services'].filter(user=self.request.user, date_add__month=value).order_by('-date_add')
        context['count'] = Services.objects.filter(user=self.request.user, date_add__month=value).aggregate(Sum('sum_for_worker'))

        return context


class ServicesDetail(LoginRequiredMixin, DetailView):
    model = Services
    context_object_name = 'service'
    template_name = 'counter/service.html'


class ServicesCreate(LoginRequiredMixin, CreateView):
    model = Services
    fields = ['price', 'sale', 'service']
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
    fields = ['price', 'sale', 'service']
    success_url = reverse_lazy('services')

    def get_context_data(self, **kwargs):
        context = super(ServicesUpdate, self).get_context_data(**kwargs)
        username = self.request.user
        context['form'].fields['service'].queryset = TypeOfWork.objects.filter(user__username=username)
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
    percent = typeser.fix_percent / 100
    sum_for_service = request.POST['price']
    end_sum = int(sum_for_service) * percent
    if request.POST.get('sale'):
        sale = request.POST['sale']
        sum_with_sale = end_sum * int(sale) / 100
        end_sum = end_sum - sum_with_sale
        return end_sum
    else:
        return end_sum
