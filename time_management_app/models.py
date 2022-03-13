from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Information(models.Model):
    date = models.DateField("日付")
    content = models.CharField("お知らせ内容", max_length=255)

    def __str__(self):
        return str(self.date)


class TimeManagement(models.Model):
    date = models.DateField("日付")
    start_time = models.TimeField("始業時刻", null=True, blank=True)
    end_time = models.TimeField("就業時刻", null=True, blank=True)
    rest_time = models.FloatField("休憩時間", null=True, blank=True)
    travel_cost = models.IntegerField("交通費", null=True, blank=True)
    travel_remarks = models.CharField("交通費_備考", max_length=255, null=True, blank=True)

    rating = models.IntegerField(
        "今日の点数",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
    )
    comment = models.CharField("振り返り", max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザー", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField("投稿日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now_add=True)

    def __str__(self):
        return str(self.created_by) + str(self.date)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "created_by"], name="date_unique_by_user"
            )
        ]
