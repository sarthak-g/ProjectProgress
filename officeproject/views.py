from django.shortcuts import render
import pyrebase
from django.contrib import auth
config = {
    "apiKey": "AIzaSyAXuTUk5ymM_nCiNMTwzMSS0cGxCUfZb10",
    "authDomain": "officeproject-b62fb.firebaseapp.com",
    "databaseURL": "https://officeproject-b62fb.firebaseio.com",
    "projectId": "officeproject-b62fb",
    "storageBucket": "officeproject-b62fb.appspot.com",
    "messagingSenderId": "525969916594"
  }
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
def signIn(request):
    return render(request,"signIn.html")
def postsign(request):
    email = request.POST.get("email")
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid credentials"
        return render(request,"signIn.html",{"messg":message})
    user = authe.refresh(user['refreshToken'])
    print(user)
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request,"welcome.html",{"e":email})
def logout(request):
    auth.logout(request)
    return render(request,"signIn.html")
def signUp(request):
    return render(request,"signup.html")
def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email,passw)
    except:
        message = "Unable to create account.TRY AGAIN."
        return render(request,"signup.html",{"messg":message})
    uid =  user['localId']
    data = {"name":name,"status":"1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")
def create(request):
    return render(request,"create.html")
def post_create(request):
    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    work = request.POST.get('work')
    progress = request.POST.get('progress')
    url = request.POST.get('url')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        "work":work,
        "progress":progress,
        "url":url
    }
    database.child("users").child(a).child("reports").child(millis).set(data)
    name = database.child("users").child(a).child("details").child("name").get().val()
    return render(request,"welcome.html",{"e":name})
