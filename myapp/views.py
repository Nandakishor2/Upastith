from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from myapp.models import *
from datetime import date,datetime

import json
import pywhatkit
from twilio.rest import Client
import threading 
day = (date.today()).weekday()
if(day == 0):
    day = "Monday"
if(day == 1):
    day = "Tuesday"
if(day == 2):
    day = "Wednesday"
if(day == 3):
    day = "Thursday"
if(day == 4):
    day = "Friday"
if(day == 5):
    day = "Saturday"
if(day == 6):
    day = "Monday"
period = ""
hr = datetime.now().hour
mi = datetime.now().minute
if (hr>8 and hr<10):
    period = "Period1"
elif (hr == 9 and mi >55) or (hr == 10 and mi <=50):
    period = "Period2"
elif (hr == 11 ) or (hr ==11 and mi<=55):
    period = "Period3"
elif (hr == 11 and mi>55 ) or (hr ==12 and mi<=50):
    period = "Period4"
elif(hr ==12 and mi>50) or (hr ==13 and mi<=30):
    period = "Lunch"
elif (hr == 13 and mi>30 ) or (hr ==14 and mi<=25):
    period = "Period5"
elif (hr == 14 and mi>25 ) or (hr ==15 and mi<=20):
    period = "Period6"
elif (hr == 15 and mi>20 ) or (hr ==16 and mi <=16):
    period = "Period7"
else :
    period = "Period1"
def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            
            login(request,user)
            
                
            return redirect("/")
        else:
            return render(request,"login.html")
    return render(request,"login.html")
def index(request):
    if request.user.is_authenticated:
        context = {
            "name":request.user,
            "period":period
        }
                    
        return render(request,"index.html",context)
    return redirect("/login")
def sendmsg(mobnum,msg):

    account_sid = 'AC8f5da5379a5dea904f3360fb9dec0512'
    auth_token = 'b3e5e4ae266dc70f1aa637e994d6b891'

    client = Client(account_sid, auth_token)

    twilio_phone_number = '+12708174402'

    recipient_phone_number = "+91"+str(mobnum) 

    

    try:
        message = client.messages.create(
            body=msg,
            from_=twilio_phone_number,
            to=recipient_phone_number
        )
        
    except Exception as e:
        pass
        



def handlelogout(request):
    fac = User.objects.get(username = str(request.user))
    stu = Faculty.objects.filter(name  =fac)
    stu.update(consulting = "")
    logout(request)
    return redirect("/login")
def loginpage(request):
    return render(request,"login.html")
def handlesignup(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password1"]
       
        myuser = User.objects.create_user(username = username,email=email,password=password)
        messages.success(request,f"Hi Your account is created ")
        return redirect("/login")
    else:
        return HttpResponse("404- Forbidden")
def updateattendence(request):
    if request.method == 'POST':
    
        data = json.loads(request.body.decode('utf-8'))
        absentiees = []
        for rows in data:
            if rows["status"] == "":
                my = Attendence(Updatedby = request.user,USN = rows["student"],Status = "Absent",Date = datetime.today()) 
                my.save()
                absentiees.append(rows)
                
            elif rows["status"] == "Absent":
                my = Attendence(Updatedby = request.user,USN = rows["student"],Status = "Absent",Date = datetime.today()) 
                absentiees.append(rows)
                my.save()
            else:
                my = Attendence(Updatedby = request.user,USN = rows["student"],Status = "Present",Date = datetime.today()) 
                
                my.save()
        
        threads = []
        for student in absentiees:
            data = Students.objects.filter(USN = student["student"])
            name = student["student"]
            for row in data:
                num = row.Contact
            thread = threading.Thread(target=sendmsg,args=[num,f"This a message from Brindavan College of Engineering is to notify that Your ward {name} is absent for {period}"])
            threads.append(thread)
            thread.start()
        for thred in threads:
            thred.join()



        return JsonResponse({"msg":"Data recieved"})
        
        
        
    
def datatopage(request):
    output = []
    


    
    classes = Schedule.objects.filter(Teacher=request.user, Day=day)
    
    for per in classes:
        
        try:
            a = getattr(per,period)
            
            if (len(a) == 1):
                students = Students.objects.filter(Sec__startswith=a)
            if (len(a)==2):
                print("I am printing",a)
                students = Students.objects.filter(Sec = a)
            
            for usn in students:
                data = {
                    "student": usn.USN,
                    "status": "" 
                }
                output.append(data)
        except:
            pass
    
    return JsonResponse({"output": output})
def attendence(request):
    return render(request,"attendence.html")
def load(request):
    if request.method == "POST":
        
        message = request.POST["message"]
        reason = request.POST["reason"]
        
        my = messagestable(From = request.user,To = "HOD",Reason = reason, Message = message,Status="Pending")  
        my.save()  
        my = Tasks(From = request.user,To = "HOD",Reason = reason, Message = message,Status="Pending") 
        my.save()
    return redirect("reqmes")   
    
def reqmes(request):
    return render(request,"reqmes.html")
def messsages(request):
    output = []
    my = messagestable.objects.filter(From = str(request.user) )
    for row in my:
        data = {
            "To" : row.To,
            "Reason" :row.Reason,
            "Message" : row.Message,
            "Status":row.Status

        }
        output.append(data)
    return JsonResponse({"output":output})    
def tasks(request):
    return render(request,"tasks.html")
def taskmessages(request):
    output = []
    my = Tasks.objects.filter(To = str(request.user) )
    for row in my:
        data = {
            "From" : row.From,
            "Reason" :row.Reason,
            "Message" : row.Message,
            "Status":row.Status

        }
        output.append(data)
    return JsonResponse({"output":output})  
def accept(request):
    
    if request.method == "POST":
        
        if request.POST["Status"] == "Accepted":
            my_queryset = messagestable.objects.filter(
                
                From=request.POST.get("From"),
                Reason=request.POST.get("Reason"),
                Message=request.POST.get("Message")
            )
            
            my_queryset.update(Status="Accepted")
            my_queryset = Tasks.objects.filter(
                
                From=request.POST.get("From"),
                Reason=request.POST.get("Reason"),
                Message=request.POST.get("Message")
            )
            for row in my_queryset:
                row.delete()
        if request.POST["Status"] == "Rejected":
            my_queryset = messagestable.objects.filter(
                
                From=request.POST.get("From"),
                Reason=request.POST.get("Reason"),
                Message=request.POST.get("Message")
            )
            
            my_queryset.update(Status="Rejected")
            my_queryset = Tasks.objects.filter(
                
                From=request.POST.get("From"),
                Reason=request.POST.get("Reason"),
                Message=request.POST.get("Message")
            )
            for row in my_queryset:
                row.delete()
            
        

    return redirect("tasks")
def notification(request):
    return render(request,"notification.html")
def search(request):
    if request.method == "GET":
        usn = request.GET["usn"]
    
    my = Students.objects.filter(USN = str(usn))
    fac = User.objects.get(username = str(request.user))
    stu = Faculty.objects.filter(name  =fac)
    stu.update(consulting = usn)
    paramia1 = {}
    paramia2 = {}
    paramia3= {}

    for row in my:
        subjects = Subjects.objects.filter(Semester = row.Semester)
        scoreia1 = Marks.objects.filter(USN = row.USN,Internal = "IA1")
        scoreia2 = Marks.objects.filter(USN = row.USN,Internal = "IA2")
        scoreia3 = Marks.objects.filter(USN = row.USN,Internal = "IA3")
        for subs in subjects:
            
            prevlage = Marks.objects.filter(USN = row.USN,SubjectName = subs.Subjectcode)
            for prev in prevlage:
                if  not prev.Input and prev.Internal == "IA1":
                    paramia1[subs.Subjectcode] = prev.Input
                if  not prev.Input and prev.Internal == "IA2":
                    paramia2[subs.Subjectcode] = prev.Input
                if  not prev.Input and prev.Internal == "IA3":
                    paramia3[subs.Subjectcode] = prev.Input
    
    print(paramia1,paramia2,paramia3)
    
    context = {"data":my,"subjects":subjects,"paramia1":paramia1,"paramia2":paramia2,"paramia3":paramia3,"Scoresia1":scoreia1,"Scoresia2":scoreia2,"Scoresia3":scoreia3,"test":["IA1","IA2","IA3"],"marksdata" :[40,60,10]}
    
    return render(request,"search.html",context)
def submitresults(request):
    subs  = []
    if request.method == "POST":
        usn = request.POST["usn"].strip()
        subject  =request.POST["subject"].strip()
        internal = request.POST["internal"]
        inp = request.POST["inp"]
        marks = request.POST["marks"]
        print(usn+subject)
        try:
            data = Marks.objects.filter(USN = usn,SubjectName = subject,Internal = internal)
            for rows in data:
                subs.append(rows.SubjectName)
        except:
            pass
        if  not (subject in subs):
            my = Marks(SubjectName = subject,USN = usn,Internal = internal,Input = inp,Score = marks)
            my.save()
        print(usn,subject,internal,inp,marks)
    return HttpResponse("Done")