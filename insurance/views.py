from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from authentication.models import Policy, PolicyUsers, Record
from user.forms import PolicyForm, RecordForm

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def profile(request):
    user = request.user
    poli_rec = PolicyUsers.objects.filter(user=user)
    policy_list = []

    for a in poli_rec:
        policy_list.append(a['policy'])

    policy_list = set(policy_list)
    return render(request, 'insurance/profile.html', {'policy_list': policy_list})


def view_record(request):
    user = request.user
    poli_rec = PolicyUsers.objects.filter(user=user)
    policy_list = []

    for a in poli_rec:
        policy_list.append(a['policy'])

    policy_list = set(policy_list)

    record_list = []
    for a in policy_list:
        records = Record.objects.filter(policy=a).all()
        record_list.extend(records)

    return render(request, 'insurance/view_record.html', {'record_list': record_list})


