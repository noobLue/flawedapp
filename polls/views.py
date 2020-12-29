from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Entry


# Create your views here.



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def sql_injection(request):

	#conn = sqlite3.connect(dbname)
	#cursor = conn.cursor()
	#response = cursor.execute("SELECT body FROM Tasks WHERE name='%s' and body LIKE '%%%s%%'" % (username, query())).fetchall()
    entry = Entry(id=1, data='secret')
    entry.save()
    
    raw = Entry.objects.raw("SELECT id FROM polls_entry WHERE id=%s" % (request.GET.get('id','')))
    try:
        sanitized = Entry.objects.get(pk=request.GET.get('id',''))
    except ValueError:
        sanitized = "not giving secret"

    return HttpResponse("raw: "+str(raw[0])+"<br/>sanitized: "+str(sanitized))