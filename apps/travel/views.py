from django.shortcuts import render, redirect
from . import models
from .models import User, Trip, UserTrip
from django.db.models import Q
import bcrypt
import datetime
import unicodedata
# Create your views here.
def index(request):
    request.session['id'] = 0
    request.session['check'] = 1
    return render(request, 'travel/index.html')

def register(request):
    request.session['check'] = 1
    request.session['message'] = []
    if len(request.POST['fullname'])<3:
        message = "Name cannot be shorter than three characters"
        request.session['message'].insert(0,message)
        request.session['check'] = 0
    if len(request.POST['username'])<3:
        message = "Username cannot be shorter than three characters"
        request.session['message'].insert(0,message)
        request.session['check'] = 0
    if len(request.POST['password'])<8:
        message = "Password must be at least eight characters"
        request.session['message'].insert(0, message)
        request.session['check'] = 0
    if request.POST['password'] != request.POST['confirm_password']:
        message = "passwords do not match"
        request.session['message'].insert(0, message)
        request.session['check']=0
    if request.session['check'] == 1:
        User.objects.create(name = request.POST['fullname'], username = request.POST['username'], password = request.POST['password'])
        user = User.objects.get(username = request.POST['username'])
        request.session['id'] = user.id
        return redirect('/travels')
    else:
        return redirect('/')

def login(request):
    request.session['message'] = []
    user = User.objects.filter(username = request.POST['username'])
    if request.POST['password'] == user[0].password:
        request.session['id'] = user[0].id
        return redirect('/travels')
    else:
        message = 'your username and password did not match our record'
        request.session['message'].insert(0, message)
        return redirect('/')

def travels(request):
    the_user = User.objects.filter(id = request.session['id'])
    user_trip = Trip.objects.filter(user__id = request.session['id'])
    print '***********************'
    print user_trip.query
    other_trips = Trip.objects.filter(~Q(user__id= request.session['id']))
    context = {'user':the_user[0], 'user_trip': user_trip, 'other_trips': other_trips}
    return render(request, 'travel/travels.html', context)


def destination(request, id):
    the_trip = Trip.objects.get(id = id)
    all_users = the_trip.user.all()
    # main_user = all_users[0]
    # main_user = all_users[len(all_users)-1]
    main_user = User.objects.get(trip_creator__the_trip__id = id)
    # main_user_id = the_trip.created_trip.the_user.id
    # main_user = User.objects.get(id = main_user_id)
    rest_users = all_users.filter(~Q(id = main_user.id))
    print '#$#$#$#$#$#$#$#$#$#'
    print rest_users.query
    context = {'user':main_user, 'users': rest_users, 'trip': the_trip}
    return render(request, 'travel/destination.html', context)

def add(request):
    return render(request, 'travel/add.html')

def inserting(request):
    request.session['checking'] = 1
    request.session['tmessage'] = []
    destination = request.POST.get('tdestination', '')
    description = request.POST.get('tdescription','')
    from_date = request.POST.get('from', datetime.datetime.now())
    print "this is the from date%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print from_date
    print datetime.datetime.now().strftime("%Y-%m-%d")
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    # from_date_unicode = request.POST.get('from', datetime.datetime.now())
    # from_date = unicodedata.normalize('NFKD', from_date_unicode).encode('ascii','ignore')

    to_date = request.POST.get('to', datetime.datetime.now())
    if len(destination)<1 or len(description)<1:
        message = 'please make sure that your destination and description is not empty'
        request.session['tmessage'].insert(0, message)
        request.session['checking'] = 0
    if from_date>to_date:
        message = 'to-date cannot be before from-date'
        request.session['tmessage'].insert(0,message)
        request.session['checking'] = 0
    if from_date<datetime.datetime.now().strftime("%Y-%m-%d"):
        message = "we don't have time machines, please pick future dates ;)"
        request.session['tmessage'].insert(0, message)
        request.session['checking'] = 0

    if request.session['checking'] == 1:
        the_user = User.objects.get(id = request.session['id'])
        Trip.objects.create(destination = request.POST['tdestination'], description = request.POST['tdescription'], date_from = request.POST['from'], date_to = request.POST['to'])
        the_trip = Trip.objects.get(destination = request.POST['tdestination'])
        the_trip.user.add(the_user)
        UserTrip.objects.create(the_user = the_user, the_trip = the_trip)
        return redirect('/travels')
    else:
        return redirect('/travels/add')


def join(request, id):
    the_trip = Trip.objects.get(id = id)
    the_user = User.objects.get(id = request.session['id'])
    the_trip.user.add(the_user)
    return redirect('/travels')
