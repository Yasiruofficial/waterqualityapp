from django.http import HttpResponse
import pickle

from api.models import Data
from api.models import Subscriber


def ml_predict_mobile(request):
    api_key = "95d465b0-0e99-4619-9553-186c4b5d294e"

    file_object = open('/ml/knn_model.pkl', 'rb')
    model = pickle.load(file_object)

    predict = model.predict([[21, 32, 45]])
    output = int(predict[0])
    print(output)

    mobile = request.GET['mobile']
    subscriber = Subscriber.filter(phone_number=mobile)
    latest_data = Data.filter(device_id=subscriber.device_id).order_by('-started_date')

