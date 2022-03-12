from django.http import JsonResponse
from time_management_app.models import TimeManagement


def get_ratings(request):
    response_data = {"id": [], "message": "good!", "ratings": []}

    objs = TimeManagement.objects.all()
    for obj in objs:
        response_data["id"].append(obj.id)
        if obj.rating is None:
            response_data["ratings"].append(0)
        else:
            response_data["ratings"].append(obj.rating)

    return JsonResponse(response_data)
