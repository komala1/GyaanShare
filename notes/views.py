from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
from datetime import date
# Create your views here.

def about(request):
    return render(request,'about.html')

def index(request):
    return render(request,'index.html')

def contact(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fullname']
        em = request.POST['email']
        m = request.POST['mobile']
        s = request.POST['subject']
        msg = request.POST['message']
        try:

            Contact.objects.create(fullname=f, email=em, mobile=m, subject=s, message=msg,msgdate=date.today(),isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request, 'contact.html', locals())

def userlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'login.html', locals())

def login_admin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error ="yes"
        except:
            error = "yes"
    return render(request,'login_admin.html', locals())

def signup1(request):
    error=""
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        e = request.POST['emailid']
        p = request.POST['password']
        b = request.POST['branch']
        r = request.POST['role']
        try:
            user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user, contact=c,branch=b,role=r)
            error="no"
        except:
            error="yes"
    return render(request,'signup.html', locals())

def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    pn = Notes.objects.filter(status="pending").count()
    an = Notes.objects.filter(status="Accept").count()
    rn = Notes.objects.filter(status="Reject").count()
    alln = Notes.objects.all().count()
    d = {'pn':pn,'an':an,'rn':rn,'alln':alln}
    return render(request,'admin_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)


    d = {'data':data,'user':user}
    return render(request,'profile.html',d)

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)
    error = False
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        b = request.POST['branch']
        user.first_name = f
        user.last_name = l
        data.contact = c
        data.branch = b
        user.save()
        data.save()
        error=True

    d = {'data':data,'user':user,'error':error}
    return render(request,'edit_profile.html',d)

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"

    return render(request,'changepassword.html', locals())

def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.FILES['notesfile']
        f = request.POST['filetype']
        d = request.POST['description']
        u = User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,subject=s,notesfile=n,
                                 filetype=f,description=d,status='pending')
            error="no"
        except:
            error="yes"
    return render(request,'upload_notes.html', locals())

def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user = user)

    d = {'notes':notes}
    return render(request,'view_mynotes.html',d)

def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return  redirect('view_mynotes')

def view_allnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user = user)

    d = {'notes':notes}
    return render(request,'view_allnotes.html',d)

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users = Signup.objects.all()

    d = {'users':users}
    return render(request,'view_users.html',d)

def delete_users(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_users')

def pending_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status = "pending")
    d = {'notes':notes}
    return render(request, 'pending_notes.html',d)

def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status = "Accept")
    d = {'notes':notes}
    return render(request, 'accepted_notes.html',d)

def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status = "Reject")
    d = {'notes':notes}
    return render(request, 'rejected_notes.html',d)

def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.all()
    d = {'notes':notes}
    return render(request, 'all_notes.html',d)

def assign_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.get(id=pid)
    error = ""
    if request.method=='POST':
        s = request.POST['status']
        try:
            notes.status = s
            notes.save()
            error="no"
        except:
            error="yes"
    d = {'notes':notes,'error':error}
    return render(request, 'assign_status.html',d)

def delete_notes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return  redirect('all_notes')

def viewallnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.filter(status='Accept')
    d = {'notes':notes}
    return render(request, 'viewallnotes.html',d)

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        try:
            if user.check_password(o):
                user.set_password(n)

                user.save()

                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'change_passwordadmin.html', locals())

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html', locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html', locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())





# Summary of views.py
# The views.py file in Django defines the logic for handling various user interactions and rendering appropriate templates for a note-sharing application. It includes functions for user authentication, profile management, note uploading, viewing, editing, and administrative tasks like managing users and note statuses.

# Functions in views.py

# about
# Summary: Renders the About page.
# Functionality: Returns the about.html template.

# index
# Summary: Renders the Index (home) page.
# Functionality: Returns the index.html template.

# contact
# Summary: Handles contact form submissions.
# Functionality: Captures contact form data and creates a Contact object, rendering the contact.html template with success or error messages.

# userlogin
# Summary: Authenticates and logs in a user.
# Functionality: Checks user credentials and logs in the user if valid, otherwise displays an error message.

# login_admin
# Summary: Authenticates and logs in an admin user.
# Functionality: Checks admin credentials and logs in the user if they have staff status, otherwise displays an error message.

# signup1
# Summary: Handles user registration.
# Functionality: Creates a new User and associated Signup object from form data, rendering the signup.html template with success or error messages.

# admin_home
# Summary: Displays the admin home page with note statistics.
# Functionality: Provides counts of notes in different statuses and renders the admin_home.html template.

# Logout
# Summary: Logs out the current user.
# Functionality: Logs out the user and redirects to the index page.

# profile
# Summary: Displays the user's profile.
# Functionality: Fetches and displays the user's profile information if authenticated, rendering the profile.html template.

# edit_profile
# Summary: Allows users to edit their profile.
# Functionality: Updates user profile information from form data and renders the edit_profile.html template with success or error messages.

# changepassword
# Summary: Allows users to change their password.
# Functionality: Changes the user's password if the new and confirm passwords match, rendering the changepassword.html template with success or error messages.

# upload_notes
# Summary: Allows users to upload notes.
# Functionality: Captures note details from form data and creates a Notes object with a pending status, rendering the upload_notes.html template with success or error messages.

# view_mynotes
# Summary: Displays notes uploaded by the logged-in user.
# Functionality: Fetches and displays the user's notes, rendering the view_mynotes.html template.

# delete_mynotes
# Summary: Allows users to delete their notes.
# Functionality: Deletes a specific note by its ID and redirects to the user's notes view.

# view_allnotes
# Summary: Displays all notes related to the logged-in user.
# Functionality: Fetches and displays all notes related to the user, rendering the view_allnotes.html template.

# view_users
# Summary: Displays all users for admin.
# Functionality: Fetches and displays all user profiles, rendering the view_users.html template for admin.

# delete_users
# Summary: Allows admin to delete users.
# Functionality: Deletes a user by their ID and redirects to the users view.

# pending_notes
# Summary: Displays notes with pending status for admin.
# Functionality: Fetches and displays notes with a pending status, rendering the pending_notes.html template.

# accepted_notes
# Summary: Displays accepted notes for admin.
# Functionality: Fetches and displays notes with an accepted status, rendering the accepted_notes.html template.

# rejected_notes
# Summary: Displays rejected notes for admin.
# Functionality: Fetches and displays notes with a rejected status, rendering the rejected_notes.html template.

# all_notes
# Summary: Displays all notes for admin.
# Functionality: Fetches and displays all notes, rendering the all_notes.html template.

# assign_status
# Summary: Allows admin to change the status of a note.
# Functionality: Updates the status of a specific note based on form data, rendering the assign_status.html template with success or error messages.





