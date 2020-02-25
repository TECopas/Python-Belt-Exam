from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages
import bcrypt

# Create your views here.
def main(request):
    return render(request,"main.html")

def index(request):
    return redirect("/main")

def travels(request):
    if "logged_in_ID" not in request.session:
        return redirect("/")

    logged_user= User.objects.get(id=request.session["logged_in_ID"]) #This works
    mytrips= Trip.objects.filter(planner = logged_user) | Trip.objects.filter(attendee = logged_user) # This seems to work, but it is the first time I've used an or "|" statement in Python such as this.
    joinabletrips = Trip.objects.exclude(attendee = logged_user) & Trip.objects.exclude(planner = logged_user) #This particular aspect is not functioning correctly, and I am not entirely sure why. An attendee of a trip should have the trip removed from the joinabletrips list.
    context = {
        "logged_user":logged_user,
        "mytrips":mytrips,
        "joinabletrips":joinabletrips
    }
    return render(request,"travels.html",context)

def register(request):
    errors = User.objects.regvalidator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    password = request.POST["Password"]
    encryptedpassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
    name=request.POST["Name"], 
    username=request.POST["Username"], 
    password = encryptedpassword)
    request.session["logged_in_ID"] = user.id
    return redirect("/travels")

def login(request):
    errors = User.objects.loginvalidator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/")
    user = User.objects.filter(username=request.POST['Username'])
    if user:
        logged_user=user[0]
        if bcrypt.checkpw(request.POST["Password"].encode(), logged_user.password.encode()):
            request.session["logged_in_ID"] = logged_user.id
            return redirect("/travels")
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def destination(request, id):
    destinfo = Trip.objects.get(id=id)
    context ={
        "destinfo":destinfo
    }
    return render(request, "destination.html", context)

def add_dest_page(request):
    if "logged_in_ID" not in request.session:
        return redirect("/")
    logged_user= User.objects.get(id=request.session["logged_in_ID"])
    context = {
        "logged_user":logged_user
    }
    return render(request, "adddest.html", context)

def adddest(request):
    errors = Trip.objects.tripvalidator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/travels/add")
    else:
        Trip.objects.create(destination=request.POST["Destination"], planner=User.objects.get(id=request.POST["PostID"]),description=request.POST["Description"], TDFrom=request.POST["TravelDateFrom"], TDTo=request.POST["TravelDateTo"])
    return redirect("/travels")

def join(request, id):
    logged_user= User.objects.get(id=request.session["logged_in_ID"])
    desired_trip=Trip.objects.get(id=id)
    desired_trip.attendee.add(logged_user)
    return redirect("/travels")

def destination(request, id):
    destination = Trip.objects.get(id=id)
    context = {
        "destination":destination
    }
    return render(request, "destination.html", context)