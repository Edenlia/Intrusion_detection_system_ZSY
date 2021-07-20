from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponse

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.core.serializers.json import DjangoJSONEncoder


@csrf_exempt
def login(request):
    dic = {'message': "hello"}
    return HttpResponse(json.dumps(dic))
