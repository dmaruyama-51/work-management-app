from sqlite3 import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import FileResponse

from time_management_app.models import TimeManagement
from time_management_app.forms import TimeManagementForm

import datetime 
import pandas as pd
import time


@method_decorator(login_required, name='dispatch')
class Home(ListView):
    paginate_by = 10
    model = TimeManagement
    template_name = 'index.html'

    def get_queryset(self):
        current_user = self.request.user
        return TimeManagement.objects.filter(created_by=current_user).order_by('-date')

    def get_context_data(self):
        context = super().get_context_data()
        context['username'] = self.request.user 
        return context 


@method_decorator(login_required, name='dispatch')
class New(View):
    def get(self, request):
        form = TimeManagementForm()
        context = {'form': form}
        return render(request, 'new.html', context)

    def post(self, request):
        form = TimeManagementForm(request.POST)

        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.created_by = request.user
                obj.save()
                return redirect('time_management:detail', id=obj.pk)
            except IntegrityError:
                error_msg = '日付を重複して登録することはできません。'
                form = TimeManagementForm()
                context = {'form': form, 'error_msg': error_msg}
                return render(request, 'new.html', context)
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
            try:
                obj = form.save(commit=False)
                obj.created_by = request.user
                obj.save()
                return redirect('time_management:detail', id=obj.pk)
            except IntegrityError:
                error_msg = '日付を重複して登録することはできません。'
                form = TimeManagementForm(instance=obj)
                context = {'form': form, 'error_msg': error_msg}
                return render(request, 'edit.html', context)
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

def file_download(request, month='this'):
    today = datetime.datetime.today()
    this_month = datetime.datetime(today.year, today.month, 1)
    last_month = this_month + datetime.timedelta(days=-1)

    if month == 'this':
        target_month = this_month.strftime('%Y%m')
    else:
        target_month = last_month.strftime('%Y%m')

    current_user = request.user
    objs = TimeManagement.objects.filter(created_by=current_user)
    records = []
    for obj in objs:
        date = obj.date
        if date.strftime('%Y%m') == target_month:
            start = obj.start_time
            end = obj.end_time 
            rest = obj.rest_time
            records.append([date, start, end, rest])
        else:
            continue
    
    records_df = pd.DataFrame(records, columns=['date', 'start', 'end', 'rest'])
    records_df.to_csv('./static/report.csv')

    time.sleep(3)

    filepath = './static/report.csv'
    filename = 'reports.csv'
    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)


