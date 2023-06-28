from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User 


def home(request):
	if request.user.is_authenticated:
		form = MeepForm(request.POST or None)
		if request.method == 'POST':
			if form.is_valid:
				meep = form.save(commit=False)
				meep.user = request.user 
				meep.save()
				messages.success(request, ('Your meep has been saved successfully!'))
				return redirect('home')
		meeps =  Meep.objects.all().order_by('created_at')
		return render(request, 'home.html', {'meeps':meeps, 'form':form})
	else:
		meeps =  Meep.objects.all().order_by('created_at')
		return render(request, 'home.html', {'meeps':meeps})
   

def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {'profiles':profiles})
	else:
		messages.success(request, ('You must be logged in to view profile list!'))
		return redirect('home')


def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		meeps = Meep.objects.filter(user_id=pk).order_by('created_at')
		if request.method == 'POST':
			current_user_profile = request.user.profile 
			action = request.POST['follow']
			if action == 'unfollow':
				current_user_profile.follows.remove(profile)
			elif action =='follow':
				current_user_profile.follows.add(profile)
			current_user_profile.save()
		return render(request, 'profile.html', {'profile':profile, 'meeps':meeps})
	else:
		messages.success(request, ('You must be logged in to view profile list!'))
		return redirect('home') 

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You must be logged in, start tweeting!'))
			return redirect('home')
		else:
			messages.success(request, ('There was an error logging in, please try again!'))
			return redirect('login')

	else:
		return render(request, 'login.html', {})



def logout_user(request):
	logout(request)
	messages.success(request, 'You are logged out successfully!')
	return redirect('home')



def register_user(request):
	form = SignUpForm(request.POST)
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			login(request, user)
			messages.success(request, ('You have successfully registered, welcome!'))
			return redirect('home')
	return render(request, 'register.html', {'form':form})
		 


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			login(request, current_user)
			messages.success(request, ('Your profile has been updated successfully!'))
			return redirect('home')
		return render(request, 'update.html', {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ('You need to login to view this page!'))
		return redirect('home')



def meep_like(request, pk):
	if request.user.is_authenticated:
		meep = get_object_or_404(Meep, id=pk)
		if meep.likes.filter(id=request.user.id):
			 meep.likes.remove(request.user)
		else:
			meep.likes.add(request.user)
		return redirect(request.META.get('HTTP_REFERER'))
	else:
		messages.success(request, ('You need to login to view this page!'))
		return redirect('home')



def meep_display(request, pk):
	meep = get_object_or_404(Meep, id=pk)
	if meep:
		
		return render(request, 'meep_display.html', {'meep':meep})
	else:
		messages.success(request, ('That meep has been deleted!'))
		return redirect('home')
