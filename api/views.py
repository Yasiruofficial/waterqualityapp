import json
import os
import sys
from django.http import HttpResponse
import pickle
from datetime import datetime

from django.shortcuts import render

from api.models import Data, Device, Subscriber, Location

sys.path.insert(1, os.path.dirname(__file__))

api_key_im = "95d465b00e9946199553186c4b5d294e"
api_key_arduino = "ebfb7ff0b2f641c8bef34fba17be410c"
requestObj = {}


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def predict_im(request):
    if 'api_key' in request.GET and \
            'mobile' in request.GET:

        if request.GET["api_key"] == api_key_im:

            mobile = request.GET['mobile']
            file_object = open(os.path.dirname(__file__) + '/ml/knn_model.pkl', 'rb')
            model = pickle.load(file_object)

            try:

                subscriber = Subscriber.objects.get(phone_number=mobile)
                latest_data = Data.objects.filter(device_id=subscriber.device_id).order_by('-time')[0]

                predict = model.predict([[
                    int(latest_data.tm),
                    int(latest_data.hu),
                    int(latest_data.wt)
                ]])

                requestObj['message'] = 'success'
                requestObj['value'] = int(predict[0])
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except Subscriber.DoesNotExist:

                requestObj['message'] = 'error'
                requestObj['value'] = 'user not found'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except IndexError:

                requestObj['message'] = 'error'
                requestObj['value'] = 'no data found on that device'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except:

                requestObj['message'] = 'error'
                requestObj['value'] = str(sys.exc_info()[0])
                return HttpResponse(json.dumps(requestObj), content_type="application/json")


        else:
            requestObj['message'] = 'error'
            requestObj['value'] = 'Unauthorized access'
            return HttpResponse(json.dumps(requestObj), content_type="application/json")

    else:
        requestObj['message'] = 'error'
        requestObj['value'] = 'incorrect request type'
        return HttpResponse(json.dumps(requestObj), content_type="application/json")


def current_data_im(request):
    if 'api_key' in request.GET and \
            'mobile' in request.GET:

        if request.GET["api_key"] == api_key_im:

            mobile = request.GET['mobile']

            try:

                subscriber = Subscriber.objects.get(phone_number=mobile)
                latest_data = Data.objects.filter(device_id=subscriber.device_id).order_by('-time')[0]
                device = Device.objects.get(id=subscriber.device_id)
                location = Location.objects.get(id=device.location_id)

                requestObj['message'] = 'success'
                requestObj['value'] = {
                    'turbidity level': int(latest_data.tm),
                    'humidity level': int(latest_data.hu),
                    'water level': int(latest_data.wt),
                    'location' : location.name
                }
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except Subscriber.DoesNotExist:

                requestObj['message'] = 'error'
                requestObj['value'] = 'user not found'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except IndexError:

                requestObj['message'] = 'error'
                requestObj['value'] = 'no data found on that device'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except:

                requestObj['message'] = 'error'
                requestObj['value'] = str(sys.exc_info()[0])
                return HttpResponse(json.dumps(requestObj), content_type="application/json")


        else:
            requestObj['message'] = 'error'
            requestObj['value'] = 'authorized access'
            return HttpResponse(json.dumps(requestObj), content_type="application/json")

    else:
        requestObj['message'] = 'error'
        requestObj['value'] = 'incorrect request type'
        return HttpResponse(json.dumps(requestObj), content_type="application/json")


# Register from Idea-mart
def reg_im(request):
    if 'api_key' in request.GET and \
            'mobile' in request.GET and \
            'device_id' in request.GET:

        if request.GET["api_key"] == api_key_im:

            mobile = request.GET['mobile']
            device_id = request.GET['device_id']

            try:

                if Subscriber.objects.filter(phone_number=mobile).count() == 0:
                    device = Device.objects.get(id=device_id)

                    subscriber = Subscriber()
                    subscriber.phone_number = mobile
                    subscriber.device_id = device.id
                    subscriber.save()

                    requestObj['message'] = 'success'
                    requestObj['value'] = 'successfully registered'
                    return HttpResponse(json.dumps(requestObj), content_type="application/json")

                requestObj['message'] = 'error'
                requestObj['value'] = 'user already in'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except Device.DoesNotExist:
                requestObj['message'] = 'error'
                requestObj['value'] = 'no device found'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except:
                requestObj['message'] = 'error'
                requestObj['value'] = str(sys.exc_info()[0])
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

        else:
            requestObj['message'] = 'error'
            requestObj['value'] = 'Unauthorized access'
            return HttpResponse(json.dumps(requestObj), content_type="application/json")

    else:

        requestObj['message'] = 'error'
        requestObj['value'] = 'incorrect request type'
        return HttpResponse(json.dumps(requestObj), content_type="application/json")


def send_data_arduino(request):
    if 'api_key' in request.GET and \
            'tm' in request.GET and \
            'hu' in request.GET and \
            'wt' in request.GET and \
            'device_id' in request.GET:

        if request.GET["api_key"] == api_key_arduino:

            tm = request.GET['tm']
            hu = request.GET['hu']
            wt = request.GET['wt']
            device_id = request.GET['device_id']

            data = Data(
                tm = tm,
                hu = hu,
                wt = wt,
                time = datetime.now(),
                device_id = device_id
            )
            data.save()
            return HttpResponse("Success")

