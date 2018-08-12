from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from authentication.models import Policy, PolicyUsers, Record
from user.crypto import get_alice, get_seed, get_bob
from user.forms import PolicyForm, RecordForm

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


import binascii
import datetime
import logging
import sys

import maya

from nucypher.characters import Alice, Bob, Ursula
from nucypher.data_sources import DataSource
# This is already running in another process.
from nucypher.network.middleware import RestMiddleware
from umbral.keys import UmbralPublicKey


def profile(request):
    user = request.user
    policy_list = Policy.objects.filter(creator=user).all()
    return render(request, 'user/profile.html', {'policy_list': policy_list})


def view_receiver(request, pk):
    receivers = PolicyUsers.objects.filter(policy=pk).all()
    receiver_list = []
    for a in receivers:
        receiver_list.append(a['user'])

    return render(request, 'user/profile.html', {'receiver_list': receiver_list})


def add_receiver(request, pk):
    user = request.user
    if request.method == 'POST':
        receiver = request.POST.get('receiver')
        if user.username == receiver or len(User.objects.filter(username=receiver).all()) == 0:
            messages.add_message(request,
                                 messages.ERROR,
                                 "Invalid User!")
        else:
            poli_rec = PolicyUsers(policy=pk, user= receiver)
            poli_rec.save()

            policy_end_datetime = maya.now() + datetime.timedelta(days=5)
            m = 2
            n = 3
            label = poli_rec.policy.label.encode('UTF-8')

            ALICE = get_alice()
            BOB = get_bob()
            alices_pubkey_bytes_saved_for_posterity = user.profile.public_key
            policy = ALICE.grant(BOB, label, m=m, n=n,
                                 expiration=policy_end_datetime)

            BOB.join_policy(label,  # The label - he needs to know what data he's after.
                            alices_pubkey_bytes_saved_for_posterity,
                            # To verify the signature, he'll need Alice's public key.
                            # He can also bootstrap himself onto the network more quickly
                            # by providing a list of known nodes at this time.
                            node_list=[("localhost", 3601)]
                            )


            messages.add_message(request,
                                 messages.SUCCESS,
                                 "Receiver added successfully.")
            return redirect('user:profile')

    return render(request, 'user/add_receiver.html', {'policy': pk})


def add_policy(request):
    user = request.user
    if request.method == 'POST':
        print ("Policy form validating.")
        form = PolicyForm(request.POST)
        if not form.is_valid():
            print ("Policy form is not valid.")
            return render(request, 'user/add_policy.html',
                      {'form': PolicyForm()})

        else:
            policy = form.save(commit=False)
            policy.creator = user
            policy.save()

            messages.add_message(request,
                                     messages.SUCCESS,
                                     "Policy added successfully.")
            return redirect('user:profile')

    print ("Rendering policy form")
    return render(request, 'user/add_policy.html',
                      {'form': PolicyForm()})


def add_record_policy(request, pk):
    user = request.user
    if request.method == 'POST':
        print("Record form validating.")
        form = RecordForm(request.POST)
        if not form.is_valid():
            print("Record form is not valid.")
            return render(request, 'user/add_record.html',
                          {'form': RecordForm()})

        else:
            record = form.save(commit=False)
            record.policy = pk
            record.save()

            messages.add_message(request,
                                 messages.SUCCESS,
                                 "Record added successfully.")
            return redirect('user:profile')

    print("Rendering policy form")
    return render(request, 'user/add_record.html',
                  {'form': RecordForm(initial={'policy': pk})})


def add_record(request):
    user = request.user
    if request.method == 'POST':
        print("Record form validating.")
        form = RecordForm(request.POST)
        if not form.is_valid():
            print("Record form is not valid.")
            return render(request, 'user/add_record.html',
                          {'form': RecordForm()})

        else:
            record = form.save(commit=False)
            record.save()

            messages.add_message(request,
                                 messages.SUCCESS,
                                 "Record added successfully.")
            return redirect('user:profile')

    print("Rendering policy form")
    return render(request, 'user/add_record.html',
                  {'form': RecordForm()})


def view_record(request):
    record_list = Record.objects.filter(policy__creator= request.user)
    return render(request, 'user/view_record.html', {'record_list': record_list})


