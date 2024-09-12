from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd

# Create your views here.


def auth(request):
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


def home(request):
    if request.user.is_authenticated:
        allevents=EventInformation.objects.all()
        allformdata=FormData.objects.all()
        print(allevents)
        return render(request, "home.html",{'event':allevents,'zip_event_form':zip(allevents,allformdata)})
        
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
    return render(request, "Manager_form.html", {'file': file, 'pk': pk})
    # return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def event_info(request):
    if request.method == "POST":
        eventname = request.POST.get("eventname")
        eventorganizer = request.POST.get("eventorganizer")
        eventday = request.POST.get("eventday")
        eventdate = request.POST.get("eventdate")
        eventtime = request.POST.get("eventtime")
        eventabout = request.POST.get("eventabout")
        file = request.FILES['file']

        fileobj = FileSystemStorage()
        filepathname = fileobj.save(file.name, file)
        filepathname = fileobj.url(filepathname)

        eventobj = EventInformation(eventname=eventname, eventorganizer=eventorganizer, eventday=eventday, eventdate=eventdate,
                                    eventtime=eventtime, eventabout=eventabout, user=request.user, eventfile=file, fileurl=file.name)
        eventobj.save()

        return redirect(f"/create_form/{file.name}/{eventobj.pk}")

    return render(request, "event_registration.html")

def event_form(request,url):
    return JsonResponse(url)
    