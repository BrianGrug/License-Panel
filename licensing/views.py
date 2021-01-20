
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.shortcuts import render

from license_django import settings
from licensing.models import LicenseHelper
from . import models
import random
import string
from ipware import ip
from django.contrib.auth.decorators import login_required


# /licensing
def index(request):
    return render(request, 'index.html')

def add(request):
    if request.method != "POST":
        return render(request, 'add.html')
    else:
        key = str(''.join((random.choice(string.ascii_letters)) for i in range(32)))
        discord = request.POST.get("discord")
        software = str(request.POST.get("software")).lower()
        collection = LicenseHelper.get_collection(software)

        if collection is None:
            return render(request, 'add.html', {
                'context': {
                    'error': 'Invalid software.'
                }
            })

        if LicenseHelper.license_exists(key, software):
            key = str(''.join((random.choice(string.ascii_letters)) for i in range(32)))

        collection.insert_one({"key": key, "discord": discord})

        return render(request, 'add.html', {
            'context': {
                'key': key,
                'discord': discord
            }
        })
@login_required
def revoke(request):
    if request.method != "POST":
        return render(request, 'revoke.html')
    else:
        key = request.POST.get("key")
        software = str(request.POST.get("software")).lower()

        collection = LicenseHelper.get_collection(software)

        if collection is None:
            return render(request, 'revoke.html', {
                'context': {
                    'error': 'Invalid software.'
                }
            })

        if not LicenseHelper.license_exists(key, software):
            return render(request, 'revoke.html', {
                'context': {
                    'error': 'License key does not exist.'
                }
            })

        collection.delete_one({"key": key})

        return render(request, 'revoked.html', {
            'context': {
                'key': key,
            }
        })

@login_required
def g_discord(request):
    if request.method != "POST":
        return render(request, 'discord.html')
    else:
        key = request.POST.get("key")
        software = str(request.POST.get("software")).lower()

        collection = LicenseHelper.get_collection(software)

        if collection is None:
            return render(request, 'discord.html', {
                'context': {
                    'key': 'Invalid software.'
                }
            })

        result = "Invalid"

        result = LicenseHelper.get_discord(key, software)

        return render(request, 'license.html', {
            'context': {
                'result': result
            }
        })

@login_required
def logs(request):
    if request.method != "POST":
        return render(request, 'logs.html')
    else:
        logs_render = LicenseHelper.get_logs()

        return render(request, 'log.html', {
            'context': {
                'logs': logs_render
            }
        })

@csrf_exempt
def validate(request):
    if request.method != "POST":
        return render(request, 'validate.html')
    else:
        password = request.POST.get("password")

        if password != "17011525":
            return render(request, 'validate.html', {
                'context': {
                    'error': 'Invalid password.'
                }
            })

        key = request.POST.get("key")
        software = str(request.POST.get("software")).lower()

        collection = LicenseHelper.get_collection(software)

        discord = LicenseHelper.get_discord_license(key, software)

        if collection is None:
            return render(request, 'validate.html', {
                'context': {
                    'error': 'Invalid software.'
                }
            })

        result = "Valid"

        global output

        if not LicenseHelper.license_exists(key, software):
            result = "Invalid"

        logs = []
        docs = collection.zhub_licenses.find().limit(30)

        output = "0x1"

        for doc in docs:
            logs.append({"result": result, "key": doc['key'], "discord": doc['discord'], "ip": ip.get_ip(request), "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})

        col = settings.MONGO_DATABASE.license_logs

        output = "{\"result\": \"%s\", \"key\": \"%s\", \"discord\": \"%s\", \"ip\": \"%s\", \"date\": \"%s\"}" % (result, key, discord, ip.get_ip(request), datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        col.insert_one({
            "key": key,
            "discord": discord,
            "software": software,
            "ip": ip.get_ip(request),
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "result": result
        })

        return HttpResponse(output)
