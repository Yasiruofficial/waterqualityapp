from django.http import JsonResponse


# Create your views here.

def testapi(request):
    data = {
        'institute_name': 'Informatics Institute of Technology (IIT)',
        'project': 'sdgp',
        'project_title': 'water_quality_meter',
        'year': 2
        }
    return JsonResponse(data)
