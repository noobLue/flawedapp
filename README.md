# flawedapp

This project is a simple webapp created with python and django. The purpose of the project is to present a couple of common security flaws from [owasp's top 10 list](https://owasp.org/www-project-top-ten/). 

### LINK: https://github.com/nooblue/flawedapp
Instructions: First thing you should do is to migrate the database with "python manage.py migrate". Then after launching the app with "python manage.py runserver", go to "/polls/init" (for example http://localhost:8000/polls/init) to create the required user entries that some of these engineered flaws use. After that you should be able to follow along as I explain each of the flaws. The project contains two example users bob//password and alice//drowssap (in format: username//password).

## FLAW 1: SQL injection

The flaw is present in /polls/sql using GET parameters. Default functionality is to pass id as a GET parameter. The sql query is done as a raw query on the server. It is possible to have server execute arbitrary SQL code because the input is not sanitized. For example instead of using get parameter id=1 (/polls/sql?id=1) you can pass this sql query in the get parameter: "/polls/sql?id=1 AND 1 == 0 UNION SELECT data from polls_entry where id = 1;--" to find the secret code that is present in the data field.

This flaw can be fixed by using the internal 'sanitizer' that is present in django. Instead of doing raw sql queries, you should use something like  "Entry.objects.get(pk=request.GET.get('id'))". This is shown in the sql view in polls.views.sql_injection, by trying both raw and sanitized methods. The raw method should return "sql_secret" and sanitized method should return "not giving secret" when the earlier mentioned sql injection method is used.


## FLAW 2: Sensitive data exposure

Go to /polls/login/ to login as user: 'bob', password: 'password'. You can view the secret data associated with the account by clicking the link "profile secret" after logging in. Problem is that sensitive data is not properly secured, so you can manually view the secret of other users by going to address /accounts/profile/<secret_id> (eg. '/accounts/profile/2' (or 3) for alices secret). This secret data could be anything from social security numbers to credit card information, so securing it is pretty important. 

This problem can be fixed by changing the way the secret is queried from the database. You should be getting the secret data by using user information from the request.user object. So in the view function "logged_in_secret" you could use UserData.objects.filter(user=request.user) instead of manually using the primary key id. Leaning on tried and tested authentication/session management systems instead of creating your own is encouraged for security.


## FLAW 3: Broken authentication

To test the message functionality: Login as a user (bob//password for example), 
Send a message using "/polls/send?from=bob&to=alice&message=funny" and then view your received messages in "/polls/view". The server logic for this functionality is a bit flawed, as it allows for spoofing the sender's username. This allows you to temporarily being able to send a message as an another user, thus being a broken authentication problem. For example, after logging in as bob, you can go to "/polls/send?from=richard&to=alice&message=malice" to send a message 'from' richard to alice, containing message "malice".

This can be fixed by getting the sending user from djangos session system: request.user, instead of it being a GET parameter. So instead of trusting the user, you should rely on the session/authentication system.


## FLAW 4: Cross-site scripting

There is a big problem with viewing the messages, as the messages aren't being properly sanitized at any point. This allows you to write a message that contains HTML to an another user. The HTML is then processed at the target users browser when they view the message. By using <script> tags it's possible to even execute javascript on the receivers browser. This would for example allow such message to be crafter that would leak the receivers entire message history (or worse), to the sender of that message. For example sending a message like this: "polls/send?from=bob&to=bob&message=<script>alert(document.getElementById('messages').innerHTML)</script>" will use javascript to show an alert box that contains the received messages of the user who views it. Alert box by itself is not a real threat, but it could be replaced with a function that sends the information to an arbitrary network location, like to the attacker. This is a form of persistent html injection, which persist from session to session. It will be triggered any time the user goes to view their messages.

One way to fix this problem is to encode the special characters that are used in html (like <, >, ", ', &), so they won't be interpreted as html by the browser. & could be changed to &amp;, < to &lt;, > to &gt; and so on.


## FLAW 5: Broken Access Control

After logging in, it is possible to update user email at address: "/polls/email?user=alice&email=bob@non.bob". There are a couple of problems; Firstly GET is used instead of POST, and secondly the user is never verified to be the owner of that account. Using the previous GET parameters, bob you could change the email of alice's account to his own. 

This could be fixed by confirming the user who owns the account is the one modifying the email. Relying on djangos authentication and session system this would be quite easy. User can be gotten from the request.user property. It would also be helpful to have an additional authentication requirement when you're changing the email. 