import json
import os
import sys
from django.http import HttpResponse
import pickle
from datetime import datetime
from django.shortcuts import render

from api.models import Data, Device, Subscriber, Location

sys.path.insert(1, os.path.dirname(__file__))

api_key = "95d465b00e9946199553186c4b5d294e"
requestObj = {}


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def home(request):
    return render(request, 'imdoc.html', status=500)


def predict_im(request):
    if 'api_key' in request.GET and \
            'mobile' in request.GET:

        if request.GET["api_key"] == api_key:

            mobile = request.GET['mobile']
            file_object = open(os.path.dirname(__file__) + '/ml/knn_model.pkl', 'rb')
            model = pickle.load(file_object)

            try:

                subscriber = Subscriber.objects.get(phone_number=mobile)
                latest_data = Data.objects.filter(device_id=subscriber.device_id).order_by('-time')[0]

                predict = model.predict([[
                    float(latest_data.tm),
                    float(latest_data.hu),
                    float(latest_data.wt)
                ]])

                requestObj['message'] = 'success'

                if int(predict[0]) == 1:
                    requestObj['value'] = "As our predicting , The Risk of flooding in your area is LOW after 6 months"
                if int(predict[0]) == 2:
                    requestObj[
                        'value'] = "As our predicting , The Risk of flooding in your area is MEDIUM after 6 months"
                if int(predict[0]) == 3:
                    requestObj[
                        'value'] = "As our predicting , The Risk of flooding in your area is HIGH after 6 months"

                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except Subscriber.DoesNotExist:

                requestObj['message'] = 'error'
                requestObj['value'] = 'User Not Found. To Learn More visit http://waterqualityapp.herokuapp.com/api'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except IndexError:

                requestObj['message'] = 'error'
                requestObj['value'] = 'no data found on that device'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except:

                requestObj['message'] = 'error'
                requestObj['value'] = "Something went wrong please try again later"
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

        if request.GET["api_key"] == api_key:

            mobile = request.GET['mobile']

            try:

                subscriber = Subscriber.objects.get(phone_number=mobile)
                latest_data = Data.objects.filter(device_id=subscriber.device_id).order_by('-time')[0]
                device = Device.objects.get(id=subscriber.device_id)
                location = Location.objects.get(id=device.location_id)

                drinkable = 'no'
                if (6.5 <= float(latest_data.ph) <= 8.5) and (float(latest_data.tr) <= 5):
                    drinkable = 'yes'

                requestObj['message'] = 'success'
                requestObj['value'] = {
                    'drinkable': drinkable,
                    'temperature level': latest_data.tm,
                    'turbidity level': latest_data.tr,
                    'ph valuel': latest_data.ph,
                    'humidity level': latest_data.hu,
                    'water level': latest_data.wt,
                    'location': location.name
                }

                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except Subscriber.DoesNotExist:

                requestObj['message'] = 'error'
                requestObj['value'] = 'User Not Found. To Learn More visit http://waterqualityapp.herokuapp.com/api'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except IndexError:

                requestObj['message'] = 'error'
                requestObj['value'] = 'no data found on that device'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except:

                requestObj['message'] = 'error'
                requestObj['value'] = "Something went wrong please try again later"
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

        if request.GET["api_key"] == api_key:

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
                requestObj['value'] = 'user Already Registered'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except Device.DoesNotExist:
                requestObj['message'] = 'error'
                requestObj['value'] = 'no device found'
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

            except:
                requestObj['message'] = 'error'
                requestObj['value'] = "Wrong Keyword Detected. To Learn More About Keyword visit http://waterqualityapp.herokuapp.com/api"
                return HttpResponse(json.dumps(requestObj), content_type="application/json")

        else:
            requestObj['message'] = 'error'
            requestObj['value'] = 'Unauthorized access'
            return HttpResponse(json.dumps(requestObj), content_type="application/json")

    else:

        requestObj['message'] = 'error'
        requestObj['value'] = 'incorrect request type'
        return HttpResponse(json.dumps(requestObj), content_type="application/json")


def getDeviceDetails(request):
    if 'device_id' in request.GET:

        if request.GET["api_key"] == api_key:

            device_id = request.GET['device_id']
            latest_data = Data.objects.filter(device_id=device_id).order_by('-time')[0]

            requestObj['message'] = 'success'
            requestObj['value'] = {
                'temperature level': latest_data.tm,
                'turbidity level': latest_data.tr,
                'ph value': latest_data.ph,
                'humidity level': latest_data.hu,
                'water level': latest_data.wt
            }

            return HttpResponse(json.dumps(requestObj), content_type="application/json")
