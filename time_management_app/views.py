from re import template
from sqlite3 import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import FileResponse
from django.urls import reverse_lazy
from django.contrib import messages

from time_management_app.models import TimeManagement
from time_management_app.forms import TimeManagementForm

import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import time


@method_decorator(login_required, name="dispatch")
class Home(ListView):
    paginate_by = 10
    model = TimeManagement
    template_name = "index.html"

    def get_queryset(self):
        current_user = self.request.user
        return TimeManagement.objects.filter(created_by=current_user).order_by("-date")

    def get_context_data(self):
        context = super().get_context_data()
        context["username"] = self.request.user
        return context


@method_decorator(login_required, name="dispatch")
class New(View):
    def get(self, request):
        form = TimeManagementForm()
        context = {"form": form}
        return render(request, "new.html", context)

    def post(self, request):
        form = TimeManagementForm(request.POST)

        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.created_by = request.user
                obj.save()

                # 午前か午後かで表示メッセージを出し分ける
                current_time = datetime.datetime.today().hour

                if current_time > 12:
                    msg = "無事記録できました！今日もお疲れ様でした！"
                else:
                    msg = "無事記録できました！今日もがんばりましょう！"

                messages.add_message(request, messages.SUCCESS, msg)
                return redirect("time_management:detail", id=obj.pk)
            except:
                error_msg = "日付を重複して登録することはできません。"
                form = TimeManagementForm()
                context = {"form": form}
                messages.add_message(request, messages.ERROR, error_msg)
                return render(request, "new.html", context)
        else:
            error_msg = form.errors
            form = TimeManagementForm()
            context = {"form": form}
            messages.add_message(request, messages.ERROR, error_msg)
            return render(request, "new.html", context)


@method_decorator(login_required, name="dispatch")
class Edit(View):
    def get(self, request, id):
        obj = get_object_or_404(TimeManagement, pk=id)
        form = TimeManagementForm(instance=obj)
        context = {"form": form}
        return render(request, "edit.html", context)

    def post(self, request, id):
        obj = get_object_or_404(TimeManagement, pk=id)
        form = TimeManagementForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.created_by = request.user
                obj.save()
                messages.add_message(request, messages.SUCCESS, "編集完了です！")
                return redirect("time_management:detail", id=obj.pk)
            except:
                error_msg = "日付を重複して登録することはできません。"
                form = TimeManagementForm(instance=obj)
                context = {"form": form}
                messages.add_message(request, messages.ERROR, error_msg)
                return render(request, "edit.html", context)
        else:
            error_msg = form.errors
            form = TimeManagementForm(instance=obj)
            context = {"form": form, "error_msg": error_msg}
            messages.add_message(request, messages.ERROR, error_msg)
            return render(request, "edit.html", context)


@method_decorator(login_required, name="dispatch")
class Detail(View):
    def get(self, request, id):
        obj = get_object_or_404(TimeManagement, pk=id)
        context = {"obj": obj}
        return render(request, "detail.html", context)


class Delete(DeleteView):
    model = TimeManagement
    template_name = "delete.html"
    success_url = reverse_lazy("time_management:index")


@login_required
def file_download(request, month="this"):
    today = datetime.datetime.today()
    this_month = datetime.datetime(today.year, today.month, 1)
    last_month = this_month + datetime.timedelta(days=-1)

    if month == "this":
        target_month = this_month.strftime("%Y%m")
        target_date_start = datetime.datetime(this_month.year, this_month.month, 1)
        target_date_end = (
            target_date_start + relativedelta(months=1) + datetime.timedelta(days=-1)
        )
    else:
        target_month = last_month.strftime("%Y%m")
        target_date_start = datetime.datetime(last_month.year, last_month.month, 1)
        target_date_end = (
            target_date_start + relativedelta(months=1) + datetime.timedelta(days=-1)
        )

    # 当月の全日数
    template_df = pd.DataFrame(
        pd.date_range(start=target_date_start, end=target_date_end, freq="D")
    ).rename(columns={0: "日付"})
    template_df["日付"] = template_df["日付"]

    # db から当月のレコード抽出
    current_user = request.user
    objs = TimeManagement.objects.filter(created_by=current_user)
    records = []
    for obj in objs:
        date = obj.date
        if date.strftime("%Y%m") == target_month:
            date = pd.Timestamp(date)
            start = obj.start_time
            end = obj.end_time
            rest = obj.rest_time
            travel_cost = obj.travel_cost
            travel_remarks = obj.travel_remarks
            records.append([date, start, end, rest, travel_cost, travel_remarks])
        else:
            continue

    records_df = pd.DataFrame(
        records, columns=["日付", "開始時間", "終了時間", "休憩時間", "交通費", "備考"]
    ).sort_values("日付")
    reports_df = pd.merge(template_df, records_df, how="left", on="日付")
    reports_df.to_csv("./static/report.csv")

    time.sleep(1)

    filepath = "./static/report.csv"
    filename = "reports.csv"
    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)


class Visualize(View):
    def get(self, request):
        # 先月と今月が対象
        today = datetime.datetime.today()
        this_month = datetime.datetime(today.year, today.month, 1)
        last_month = this_month + datetime.timedelta(days=-1)

        last = last_month.strftime("%Y%m")
        this = this_month.strftime("%Y%m")

        current_user = request.user
        objs = TimeManagement.objects.filter(created_by=current_user)

        data_tmp = []
        for obj in objs:
            if (obj.date.strftime("%Y%m") == last) or (
                obj.date.strftime("%Y%m") == this
            ):
                date = obj.date.strftime("%Y-%m-%d")
                rating = obj.rating
                start = obj.start_time
                end = obj.end_time
                rest = obj.rest_time
                try:
                    work_time = (
                        datetime.datetime.strptime(str(end), "%H:%M:%S")
                        - datetime.datetime.strptime(str(start), "%H:%M:%S")
                    ).seconds // 3600 - rest
                except:
                    work_time = 0.0
                data_tmp.append([date, rating, work_time])

        df = pd.DataFrame(
            data_tmp, columns=["date", "rating", "work_time"]
        ).sort_values("date")
        context = {
            "dates": df.date.to_list(),
            "ratings": df.rating.to_list(),
            "work_time": df.work_time.to_list(),
        }

        return render(request, "visualize.html", context)
