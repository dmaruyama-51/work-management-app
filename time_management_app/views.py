from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from time_management_app.models import TimeManagement
from time_management_app.forms import TimeManagementForm


@method_decorator(login_required, name='dispatch')
class Home(ListView):
    paginate_by = 7
    model = TimeManagement
    template_name = 'index.html'

    def get_queryset(self):
        current_user = self.request.user
        return TimeManagement.objects.filter(created_by=current_user).order_by('-date')


@method_decorator(login_required, name='dispatch')
class New(View):
    def get(self, request):
        form = TimeManagementForm()
        context = {'form': form}
        return render(request, 'new.html', context)

    def post(self, request):
        form = TimeManagementForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return redirect('time_management:detail', id=obj.pk)
        else:
            error_msg = form.errors
            form = TimeManagementForm()
            context = {'form': form, 'error_msg': error_msg}
            return render(request, 'new.html', context)


@method_decorator(login_required, name='dispatch')
class Edit(View):
    def get(self, request, id):
        obj = get_object_or_404(TimeManagement, pk=id)
        form = TimeManagementForm(instance=obj)
        context = {'form': form}
        return render(request, 'edit.html', context)

    def post(self, request, id):
        obj = get_object_or_404(TimeManagement, pk=id)
        form = TimeManagementForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return redirect('time_management:detail', id=obj.pk)
        else:
            error_msg = form.errors
            form = TimeManagementForm(instance=obj)
            context = {'form': form, 'error_msg': error_msg}
            return render(request, 'edit.html', context)



@method_decorator(login_required, name='dispatch')
class Detail(View):
    def get(self, request, id):
        obj = get_object_or_404(TimeManagement, pk=id)
        context = {'obj': obj}
        return render(request, 'detail.html', context)    