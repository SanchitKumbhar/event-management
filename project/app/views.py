from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from django.forms.models import model_to_dict
# Create your views here.


def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        position = request.POST.get("position")
        user = CustomUser.objects.create(email=email)
        user.set_password(password)
        user.save()

        if user is not None:
            login(request, user)
            return redirect("/")

    return render(request, "auth.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            print('Invalid username or password.')
    return render(request, 'login.html')

def home(request):
    if request.user.is_authenticated:
        allevents=EventInformation.objects.all()
        allformdata=FormData.objects.all()
        print(allevents)
        return render(request, "home.html",{'event':allevents})

    else:
        return redirect("/auth")


def PreprocessData(formapi, file):
    schema = []
    for index in range(len(formapi)):
        key = formapi[index]
        schema.append(key.get("question"))

    df = pd.DataFrame(columns=schema)

    # # # Save the DataFrame to an Excel file
    df.to_excel(f'files/{file}', index=False)

    print("Excel file created successfully!")


def submit_form(request, file, pk):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))

        # Do something with the data (e.g., save to database, process further)
        event_instance = EventInformation.objects.get(id=pk)

        form_data = FormData(data=data, customuser=request.user, event=event_instance)
        form_data.save()

        PreprocessData(data, file)

        # Send a response back to the client
        return JsonResponse({"status": "success", "received": data})

    except json.JSONDecodeError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


def create_form(request, file, pk):

    return render(request, "manager_form.html", {'file': file, 'pk': pk})
    # return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def event_info(request):
    if request.method == "POST":
        # eventname = request.POST.get("eventname")
        eventorganizer = request.POST.get("eventOrganizer")
        eventday = request.POST.get("eventDay")
        eventdate = request.POST.get("eventDate")
        eventtime = request.POST.get("eventTime")
        eventabout = request.POST.get("eventAbout")
        file = request.FILES['file']

        fileobj = FileSystemStorage()
        filepathname = fileobj.save(file.name, file)
        filepathname = fileobj.url(filepathname)

        eventobj = EventInformation(eventname="eventname", eventorganizer=eventorganizer, eventday=eventday, eventdate=eventdate,
                                    eventtime=eventtime, eventabout=eventabout, user=request.user, eventfile=file, fileurl=file.name)
        eventobj.save()

        return redirect(f"/create_form/{file.name}/{eventobj.pk}")

    return render(request, "event_registration.html")



def form_render(request,pk):
            return render(request,"client-form.html",{'id':pk})


def formapi(request,pk):
    if request.method=='GET':
        eventinstance=EventInformation.objects.get(pk=pk)
        get_instance=FormData.objects.get(event=pk)
        print(get_instance.data[0])
        return JsonResponse(model_to_dict(get_instance))

       # print(model_to_dict(get_instance))



# this feature editing is stopped for a while
def Draft(request):
    jsondata = json.loads(request.body)
    eventinstance=EventInformation.objects.get(pk=jsondata.get('pk'))

    draftinstance=DraftModel.objects.filter(event=eventinstance).exists()

    if draftinstance is False:
        DraftModel.objects.create(user=request.user,event=eventinstance,data=jsondata.get('data'))
    else:
        draftinstance=DraftModel.objects.filter(event=eventinstance)
        DraftModel.data=jsondata.get('data')
        DraftModel.event=draftinstance
        DraftModel.user=request.user

    return JsonResponse({
        'success' : 200
    })

import openai
# large dataIntegration code:
def dataItegration(request):
    if request.method == 'POST':
        jsonMsg=json.loads(request.body)
        print(jsonMsg.get("msg"))

    return JsonResponse({
        'succ' : 'ok'
        })



# def GetDraft(request,pk):
#     if request.method == 'GET':
#         eventinstance=EventInformation.objects.get(pk=pk)
#         draftinstance=DraftModel.objects.get(event=eventinstance)
#         return JsonResponse({draftinstance.data[0]})
