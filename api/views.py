from django.http import HttpResponse

from api.models import Data, Device


def post_data(request):
    api_key = "95d465b0-0e99-4619-9553-186c4b5d294e"

    # if request.GET["api_key"] == api_key:

    #     if 'ph' in request.GET and \
    #             'us' in request.GET and \
    #             'hd' in request.GET and \
    #             'ts' in request.GET and \
    #             'device' in request.GET:

    #         data = Data()
    #         data.ph = request.GET["ph"]
    #         data.us = request.GET["us"]
    #         data.hd = request.GET["hd"]
    #         data.ts = request.GET["ts"]
    #         data.device_id = request.GET["device"]
    #         data.save()

    #         return HttpResponse(" Inserted =$= ")
    #     else:
    #         return HttpResponse(" Error on Saving =$= ")
    # else:
    return HttpResponse(" Worng API_KEY =$= ")
