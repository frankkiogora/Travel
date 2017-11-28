from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import User, Travel



def index(request):
    return render(request, 'travel_planner/index.html')

def register(request):
    newuser = User.objects.validate(request.POST)
   
    
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each) 
        return redirect('/')
    if newuser[0] == True:
        messages.success(request, 'Well done')
        request.session['id'] = newuser[1].id
        return redirect('/travel')

def login(request):
    if 'id' in request.session:
        return redirect('/travel')
    if request.method == 'GET':
        return redirect('/')
    else:
        user = User.objects.login(request.POST)
        print user
        if user[0] == False:
            for each in user[1]:
                messages.add_message(request, messages.INFO, each)
            return redirect('/')
        if user[0] == True:
            messages.add_message(request, messages.INFO,'Welcome, You are logged in!')
            request.session['id'] = user[1].id
            return redirect('/travel')


def travel(request):
    
    context = {
        "user": User.objects.get(id=request.session['id']),
        "travels" : Travel.objects.all(),
        "others": Travel.objects.all().exclude(join__id=request.session['id'])
    }
    return render(request, 'travel_planner/travelplan.html', context)


def addplan(request):
    if 'id' not in request.session:
        return redirect ("/")
    else:
        context= {
            "user":User.objects.get(id=request.session['id']),
        }
        return render(request, 'travel_planner/addplan.html', context)
# scheduling trip
def createplan(request):
    newplan= Travel.objects.travelval(request.POST, request.session["id"])
    if newplan[0] == True:
        return redirect('/travel')
    else:
        for message in newplan[1]:
            messages.error(request, message)
        return redirect('/addplan')
    
#Render profile here
def show(request, travel_id):
    try:
        travel= Travel.objects.get(id=travel_id)
    except Travel.DoesNotExist:
        messages.info(request,"Could not be found")
        return redirect('/travel')
    context={
        "travel": travel,
        "user":User.objects.get(id=request.session['id']),
        "others": User.objects.filter(joiner__id=travel.id).exclude(id=travel.creator.id),
    }
    return render(request, 'travel_planner/profile.html', context)

def join(request, travel_id):
    if request.method == "GET":
        messages.error(request,"What trip?")
        return redirect('/')
    joiner= Travel.objects.join(request.session["id"], travel_id)
    if 'errors' in joiner:
        messages.error(request, joiner['errors'])
    return redirect('/travel')
   

#destroy
def delete(request, id):
    try:
        target= Travel.objects.get(id=id)
    except Travel.DoesNotExist:
        messages.info(request,"Message Not Found")
        return redirect('/travel')
    target.delete()
    return redirect('/travel')


def logout(request):
    if 'id' not in request.session:
        return redirect('/')
    del request.session['id']
    return redirect('/')

   
    







    



