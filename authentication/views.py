from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from authentication.forms import LogInForm


@login_required(login_url='login/')
def home(request):
    return redirect_user(request, request.user)


def login_view(request):
    if request.method == 'POST':
        print ("Login form validating.")
        form = LogInForm(request.POST)
        if not form.is_valid():
            print ("Login form is not valid.")
            return render(request, 'auth/login.html',
                      {'form': LogInForm()})

        else:
            # user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    print(str(user.profile.account_type)+" Logged in.")
                    login(request,user)
                    return redirect_user(request, user)

            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     "Please enter valid username & password.")


    print ("Rendering get form")
    return render(request, 'auth/login.html',
                      {'form': LogInForm()})


def logout_view(request):
    logout(request)
    return redirect('login')


def redirect_user(request, user):
    if user.profile.account_type == 0:
        return redirect('user:profile')

    elif user.profile.account_type == 1:
        return redirect('insurance:profile')

    else:
        logout(request)