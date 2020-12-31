from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Entry, UserData, ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def logged_in(request):
    userData = UserData.objects.filter(user = request.user)

    return HttpResponse("Your name is: " + str(request.user) + ", view your secret here: <a href=/accounts/profile/" + str(userData[0].pk) + ">profile secret</a>")

@login_required
def logged_in_secret(request, secret_id):
    userData = UserData.objects.filter(pk=secret_id)

    return HttpResponse('secret: ' + str(userData[0]) )

def sql_injection(request):

	#conn = sqlite3.connect(dbname)
	#cursor = conn.cursor()
	#response = cursor.execute("SELECT body FROM Tasks WHERE name='%s' and body LIKE '%%%s%%'" % (username, query())).fetchall()
    entry = Entry(id=1, data='sql_secret')
    entry.save()
    
    raw = Entry.objects.raw("SELECT id FROM polls_entry WHERE id=%s" % (request.GET.get('id','')))
    try:
        sanitized = Entry.objects.get(pk=request.GET.get('id',''))
    except ValueError:
        sanitized = "not giving secret"

    return HttpResponse("raw: "+str(raw[0])+"<br/>sanitized: "+str(sanitized))

def init_user_data(request):
    try:
        user = User.objects.create_user('bob', 'bob@non.bob', 'password')
        user.save()
    except IntegrityError: 
        print('user exists already')
        user = User.objects.filter(username='bob')[0]

    userData = UserData.objects.get_or_create(user=user, data='bob_secret_funny')
    if(userData[1]):
        userData[0].save()

    try:
        user2 = User.objects.create_user('alice', 'alice@fake.name', 'drowssap')
        user2.save()
    except IntegrityError: 
        user = User.objects.filter(username='alice')[0]
        print('user exists already')

    userData2 = UserData.objects.get_or_create(user=user2, data='alice_secret_hilarious')
    if(userData2[1]):
        userData2[0].save()

    return(HttpResponse("Created required database data: <a href='/polls/login'>login</a>"))

def xcross_site_script(request):
    

    return(HttpResponse(""))

@login_required
def send_message(request):
    user_from = User.objects.get(username=request.GET.get('from')) #make one flaw from this: spoofing sender
    user_to = User.objects.get(username=request.GET.get('to'))
    message = request.GET.get('message')

    data = ChatMessage.objects.create(user_to=user_to, user_from=user_from, message=message)
    data.save()

    return(HttpResponse("sent message to " + str(user_to)))

@login_required
def view_messages(request):
    messages = ChatMessage.objects.filter(user_to=request.user)

    message_html = "<tag id='messages'>"
    for msg in messages:
        message_html += str(msg) + "<br/>"
    message_html += "</tag>"

    return HttpResponse(message_html)


@login_required
def change_email(request):
    user = User.objects.get(username=request.GET.get('user'))
    new_email = request.GET.get('email')

    user.email = str(new_email)
    user.save()

    return HttpResponse("changed email of user: "+str(user) + " to " + str(user.email))