from django.shortcuts import render,redirect
from .models import User
import requests
import random

# Create your views here.

def index(request):
	return render(request,'index.html')

def driver_index(request):
	return render(request,'driver-index.html')

def about(request):
	return render(request,'about.html')

def car(request):
	return render(request,'car.html')

def contact(request):
	return render(request,'contact.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=="rider":
					request.session['email']=user.email
					request.session['fname']=user.fname
					return render(request,'index.html')
				else:
					request.session['email']=user.email
					request.session['fname']=user.fname
					return render(request,'driver-index.html')
			else:
				msg="Incorrect password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email not registerd"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def signup(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			msg=" email alredy registerd"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					usertype=request.POST['usertype'],
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password']
					)
				msg="user sign up successfuly"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="password & confirmpassword does not match"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')


def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')

	except:
		return render(request,'login.html')

def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="new password & confirm new passworddoes not matches"
				if user.usertype=="rider":
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'driver-change-password.html',{'msg':msg})
		else:
			msg="old password is incoorect"
			if user.usertype=="rider":
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'driver-change-password.html',{'msg':msg})
	else:
		if user.usertype=="rider":
			return render(request,'change-password.html')
		else:
			return render(request,'driver-change-password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(mobile=request.POST['mobile'])
			mobile=request.POST['mobile']
			otp=random.randint(1000,9999)
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"gMx3lhUfb02EBRnSKZVpYNIJwivzPGr9X6kTDjm5A4ec1yW7QHMzvxJ8OkGBsUqISHrFPeLXu71Z9o3l","variables_values":str(otp),"route":"otp","numbers":str(mobile)}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			return render(request,'otp.html',{'mobile':mobile,'otp':otp})
		except:
			msg="mobile not registerd"
			return render(request,'forgot-password.html',{'msg':msg})
	else:
		return render(request,'forgot-password.html')

def verify_otp(request):
	mobile=request.POST['mobile']
	otp=int(request.POST['otp'])
	uotp=int(request.POST['uotp'])
	if otp==uotp:
		return render(request,'new_password.html',{'mobile':mobile})

	else:
		msg="Invalid otp"
		return render(request,'otp.html',{'mobile':mobile,'otp':otp,'msg':msg})

def new_password(request):
	mobile=request.POST['mobile']
	np=request.POST['new_password']
	cnp=request.POST['cnew_password']

	if np==cnp:
		user=User.objects.get(mobile=mobile)
		user.password=np
		user.save()
		msg="password update successfuly"
		return render(request,'login.html')
	else:
		msg="new password & confirm password does not match"
		return render(request,'new_password.html',{'mobile':mobile,'msg':msg})