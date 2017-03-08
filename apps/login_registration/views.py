from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User
import types

# displays a page where user can either register or log in
def index(request):
    return render(request, 'login_registration/index.html')

# registers user name, email, and password if all information is valid
def register(request):
    if request.method != 'POST':
        return redirect(reverse('login_registration:index'))
    else:
        user = User.objects.register(request.POST)
        if isinstance(user, types.ListType):
            for error in user:
                messages.error(request, error)
            if request.session['user_level'] == 9:
                return redirect(reverse('user_dashboard:add'))
            else:
                return redirect(reverse('user_dashboard:index'))
        else:
            if request.session['user_level'] != 9:
                request.session['user_id'] = user.id
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['user_level'] = user.user_level
            return redirect(reverse('user_dashboard:dashboard'))

# logs in user if user information is valid and saves information into a session
def login(request):
    if request.method != 'POST':
        return redirect(reverse('user_dashboard:index'))
    else:
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Invalid Email or Password!")
            return redirect(reverse('user_dashboard:index'))
        else:
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['user_level'] = user.user_level
            return redirect(reverse('user_dashboard:dashboard'))

# logs out a user and deletes session containing user information
def logout(request):
    User.objects.logout(request.session['user_id'])
    return redirect(reverse('user_dashboard:index'))

# displays a welcome page when a user successfully registers or logs in
def show(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'login_registration/success.html', context)

# displays a form page allowing user to edit their information
def edit(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'login_registration/edit.html', context)

# updates user information
def update(request, id):
    if request.method != 'POST':
        return redirect(reverse('user_dashboard:dashboard'))
    else:
        User.objects.update(request.POST, id, request.session['user_level'])
        return redirect(reverse('user_dashboard:dashboard'))

# deletes given User object
def destroy(request, id):
    User.objects.get(id=id).delete()
    return redirect(reverse('user_dashboard:dashboard'))
