from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from .forms import *


# Create your views here.

def index(request):
    return render(request, 'index.html')


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                return redirect('admin_home')
            else:
                error = "Retry using your admin login credentials!"
        except:
            error = "Invalid login credentials, Try again..."
    d = {'error': error}
    return render(request, 'admin_login.html', d)


def user_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                login(request, user)
                return redirect('user_home')
            except:
                error = "You are not a student"
        else:
            error = "Invalid login credentials, Try again..."
    d = {'error': error}
    return render(request, 'user_login.html', d)


def recruiter_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status != "Pending":
                    login(request, user)
                    return redirect('recruiter_home')
                else:
                    error = "You are not approved as a recruiter yet!"
            except:
                error = "Something is wrong! Please try again..."
        else:
            error = "Invalid login credentials, Try again..."
    d = {'error': error}
    return render(request, 'recruiter_login.html', d)


def recruiter_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        c = request.POST['contact']
        g = request.POST['gender']
        company = request.POST['company']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(user=user, mobile=c, image=i, gender=g, company=company, type="recruiter",
                                     status="Pending")
            # error = "no"
            return redirect('recruiter_login')

        except:
            error = "Something is wrong! Please try again..."
    d = {'error': error}
    return render(request, 'recruiter_signup.html', d)


def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        g = request.POST['gender']

        student.user.first_name = f
        student.user.last_name = l
        student.mobile = c
        student.gender = g
        try:
            student.save()
            student.user.save()
            error = "Profile Updated Successfully!"
            return redirect('user_home')

        except:
            error = "Something went wrong!!"

        try:
            i = request.FILES['image']
            student.image = i
            student.save()
            error = "Profile Updated Successfully!"
            return redirect('user_home')

        except:
            pass

    d = {'student': student, 'error': error}
    return render(request, 'user_home.html',d)


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    rcount = Recruiter.objects.all().count()
    scount = StudentUser.objects.all().count()
    d = {'rcount':rcount, 'scount':scount}
    return render(request, 'admin_home.html',d)


def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        g = request.POST['gender']

        recruiter.user.first_name = f
        recruiter.user.last_name = l
        recruiter.mobile = c
        recruiter.gender = g
        try:
            recruiter.save()
            recruiter.user.save()
            error = "Profile Updated Successfully!"
            return redirect('recruiter_home')

        except:
            error = "Something went wrong!!"

        try:
            i = request.FILES['image']
            recruiter.image = i
            recruiter.save()
            error = "Profile Updated Successfully!"
            return redirect('recruiter_home')

        except:
            pass

    d = {'recruiter': recruiter, 'error': error}
    return render(request, 'recruiter_home.html',d)


def Logout(request):
    logout(request)
    return redirect('index')


def user_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        c = request.POST['contact']
        g = request.POST['gender']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            StudentUser.objects.create(user=user, mobile=c, image=i, gender=g, type="student")
            # error = "Registered Successfully!"
            return redirect('user_login')

        except:
            error = "Something is wrong! Please try again..."
    d = {'error': error}
    return render(request, 'user_signup.html', d)


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    d = {'data': data}
    return render(request, 'view_users.html', d)


def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')


def delete_recruiter(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter = User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_all')


def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Pending')
    d = {'data': data}
    return render(request, 'recruiter_pending.html', d)


def change_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    recruiter = Recruiter.objects.get(id=pid)
    if request.method == "POST":
        s = request.POST['status']
        recruiter.status = s
        try:
            recruiter.save()
            error = "Status changed successfully!"
            return redirect('recruiter_all')
        except:
            error = "Something went wrong, Try again..."
    d = {'recruiter': recruiter, 'error': error}
    return render(request, 'change_status.html', d)


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "Password changed successfully!"
                return redirect('admin_login')
            else:
                error = "Your Current Password is wrong"
        except:
            error = "Something went wrong, Try again..."
    d = {'error': error}
    return render(request, 'change_passwordadmin.html', d)


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "Password changed successfully!"
                return redirect('user_login')
            else:
                error = "Your Current Password is wrong"
        except:
            error = "Something went wrong, Try again..."
    d = {'error': error}
    return render(request, 'change_passworduser.html', d)


def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "Password changed successfully!"
                return redirect('recruiter_login')
            else:
                error = "Your Current Password is wrong"
        except:
            error = "Something went wrong, Try again..."
    d = {'error': error}
    return render(request, 'change_passwordrecruiter.html', d)


def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Accept')
    d = {'data': data}
    return render(request, 'recruiter_accepted.html', d)


def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Reject')
    d = {'data': data}
    return render(request, 'recruiter_rejected.html', d)


def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.all()
    d = {'data': data}
    return render(request, 'recruiter_all.html', d)


def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    error = ""
    form = JobPostingForm()
    if request.method == 'POST':
        form = JobPostingForm(request.POST, request.FILES, )
        if form.is_valid:
            job = form.save(commit=False)
            user = request.user
            job.recruiter = Recruiter.objects.get(user=user)
            job.save()
            return redirect('job_list')
        else:
            error = 'yes'

    context = {'error': error, 'form': form}
    return render(request, 'add_job.html', context)


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    d = {'job': job}
    return render(request, 'job_list.html', d)


def edit_jobdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    error = ""
    job = Job.objects.get(id=pid)
    form = JobPostingForm(instance=job)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, request.FILES, instance=job)
        if form.is_valid:
            form.save()
            return redirect('job_list')
        else:
            error = 'yes'

    context = {'error': error, 'form': form, 'job': job}
    return render(request, 'add_job.html', context)

def latest_jobs(request):
    job = Job.objects.all().order_by('-start_date')
    d = {'job': job}
    return render(request, 'latest_jobs.html', d)

def user_latestjobs(request):
    job = Job.objects.all().order_by('-start_date')
    user = request.user
    student = StudentUser.objects.get(user=user)
    data = Apply.objects.filter(student=student)
    li = []
    for i in data:
        li.append(i.job.id)

    d = {'job': job, 'li' : li}
    return render(request, 'user_latestjobs.html', d)

def job_detail(request, pid):
    job = Job.objects.get(id = pid)

    d = {'job': job,}
    return render(request, 'job_detail.html', d)

def applyforjob(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')

    error = ""
    user = request.user
    student = StudentUser.objects.get(user=user)
    job = Job.objects.get(id=pid)
    date1 = date.today()
    if job.end_date < date1:
        return redirect('user_latestjobs')
        error = "Applications are closed, last date is over!"
    elif job.start_date > date1:
        return redirect('user_latestjobs')
        error = "Applications are not open yet"

    else:
        if request.method == 'POST':
            r = request.FILES['resume']
            Apply.objects.create(job=job, student=student, resume=r, applydate=date.today())
            error="Application submitted successfully"
            return redirect('user_latestjobs')

    d = {'error': error,}
    return render(request,'applyforjob.html',d)

def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    data = Apply.objects.all()

    d = {'data': data}
    return render(request,'applied_candidatelist.html',d)

def contact(request):
    return render(request, 'contact.html')