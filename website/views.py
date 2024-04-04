from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            messages.error(request, 'There was an error. Please try again.')
            return redirect('home')

    else:
        return render(request, 'home.html', {'records': records})


def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('home')
    else:
        form = SignupForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        costumer_record = Record.objects.get(pk=pk)
        return render(request, 'records.html', {'costumer_record': costumer_record})
    else:
        messages.error(request, 'You have not been logged in!')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record has been deleted!')
        return redirect('home')
    else:
        messages.error(request, 'You have not been logged in!')
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated and request.method == "POST" and form.is_valid():
        add_record = form.save()
        messages.success(request, 'Record has been added!')
        return redirect('home')
    elif request.user.is_authenticated and request.method != "POST":
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, 'You have not been logged in!')
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been updated!')
            return redirect("home")
        else:
            return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, 'You have not been logged in!')
        return redirect('home')
