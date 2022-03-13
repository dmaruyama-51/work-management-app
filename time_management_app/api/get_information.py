from urllib import response
from django.http import JsonResponse
from time_management_app.models import Information


def get_information(request):

    response_data = []

    objs = Information.objects.all()

    for obj in objs:
        response_data.append({"infoDate": str(obj.date), "infoContent": obj.content})

    # objs = TimeManagement.objects.all()
    # for obj in objs:
    #     response_data["id"].append(obj.id)
    #     if obj.rating is None:
    #         response_data["ratings"].append(0)
    #     else:
    #         response_data["ratings"].append(obj.rating)

    return JsonResponse(response_data, safe=False)
