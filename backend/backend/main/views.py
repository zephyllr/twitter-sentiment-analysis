from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from backend.main.analyze import get_analysis_result
from datetime import datetime, timedelta
from django.db.models import Q
from backend.main.update import run_update
from django.views.decorators.csrf import csrf_exempt
from random import randint
from django.views.generic import TemplateView
from datetime import datetime

def home(request):
    return render(request, 'login.html')

# clear session, return to home

def logout(request):
    request.session.delete()
    return redirect("/login")

def login(request):
    if "user" in request.session:
        return redirect("/feed")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(Q(username=username), Q(password=password))
        if not user:
            return render(request, 'login.html', {'error': 'User does not exist'})
        request.session['user'] = username
        return redirect('/feed')
    return render(request, 'login.html')

def register(request):
    if "user" in request.session:
        return redirect("/feed")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(Q(username=username))
        if user:
            return render(request, 'register.html', {'error': 'Username is taken'})

        new_user = User.objects.create(username=username, password=password)
        request.session["user"] = username
        return redirect("/feed")
    return render(request, 'register.html')

def feed(request):
    if "user" not in request.session:
        return redirect("/login")
    uname = request.session.get("user")
    user = User.objects.get(username=uname)
    subs = Subscription.objects.filter(user_id = user)    

    error = request.session.get("subscription_error") or None
    graph = request.session.get("graph") or None

    topic = request.GET.get('topic', '')

    analysis_results = []

    content = {
        'user': user.username, 
        'user_subs': subs, 
        'error': error, 
        'graph': graph,
        'timeseries': []
    }

    for sub in subs:
        # for each subscription, get analysis results
        htag = sub.hashtag_id
        analysis = Analysis.objects.filter(hashtag_id = htag)

        if (htag.topic == topic):
            topic_analysis = analysis[0].timeseries[-1].value/1000
            content['topic'] = topic
            content['topic_analysis'] = topic_analysis
            for elem in analysis[0].timeseries:
                content['timeseries'].append([(elem.time-datetime(1970,1,1)).total_seconds() * 1000, elem.value/1000])
                
        if not analysis or analysis[0].invalid_hashtag or not analysis[0].timeseries:
            analysis_results.append("N/A")
        else:
            analysis_results.append(analysis[0].timeseries[-1].value/1000)

    content['analysis_results'] = analysis_results
    return render(request, 'feed.html', content)

def subscribe(request):
    if "user" not in request.session:
        return redirect("/login")

    uname = request.session.get("user")
    user = User.objects.get(username=uname)

    if request.method == 'POST':
        topic = request.POST['topic']
        freq = request.POST['freq']
        existing_sub = Subscription.objects.filter(user_id = user).filter(hashtag_id=topic)

        if not freq.isdigit() or freq == "0":
            error = "Frequency field must be a nonzero postive integer (X days)!"
            request.session['subscription_error'] = error
        elif existing_sub:
            error = "You are already subscribed to this hashtag!"
            request.session['subscription_error'] = error
        else:
            # create or get hashtag
            new_htag = Hashtag.objects.get_or_create(topic=topic)[0]
            
            # add new subscription
            Subscription.objects.create(
                user_id=user, 
                hashtag_id=new_htag, 
                frequency=int(freq),
                last_scanned=(datetime.today() - timedelta(days=int(freq))),
            )
            request.session['subscription_error'] = None
    return redirect('/feed')

def unsubscribe(request):
    if "user" not in request.session:
        return redirect("/login")

    if request.method == 'POST':
        uname = request.session.get("user")
        user = User.objects.get(username=uname)
        topic = request.POST.get('topic')
        htag = Subscription.objects.filter(user_id = user).filter(hashtag_id=topic)

        if htag:
            htag.delete()
            request.session['subscription_error'] = None

            # delete hashtag if not dependent on other subscriptions
            target_subs = Subscription.objects.filter(hashtag_id = topic)
            if not target_subs:
                Hashtag.objects.get(topic=topic).delete()

        else:
            error = "Subscription does not exist"
            request.session['subscription_error'] = error

    return redirect('/feed')

def analyze(request):
    if "user" not in request.session:
        return redirect("/login")

    uname = request.session.get("user")
    user = User.objects.get(username=uname)
    topic = request.GET.get('topic')
    sub = Subscription.objects.filter(user_id = user).filter(hashtag_id=topic)
    concat = '/feed'
    
    if sub:
        htag = Hashtag.objects.get(topic=topic)
        analysis = Analysis.objects.filter(hashtag_id = htag)
        if analysis:
            # no tweets for this hashtag
            if analysis[0].invalid_hashtag:
                request.session['graph'] = False 
                error = "No past tweets were found for this hashtag."
                request.session['subscription_error'] = error
            # analysis found for this hashtag
            else:
                request.session['graph'] = True 
                request.session['subscription_error'] = None
                concat = '/feed?topic=' + topic
        # subcription time has not come 
        else:
            request.session['graph'] = False 
            error = "Your graphs for this subscription are not availble until your requested time."
            request.session['subscription_error'] = error
    # invalid subscription
    else:
        request.session['graph'] = False 
        error = "You are not subscribed to this hashtag"
        request.session['subscription_error'] = error
    return redirect(concat)
    