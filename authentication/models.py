from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# import binascii
# import datetime
# import logging
# import sys
#
# import maya
#
# from nucypher.characters import Alice, Bob, Ursula
# from nucypher.data_sources import DataSource
# # This is already running in another process.
# from nucypher.network.middleware import RestMiddleware
# from umbral.keys import UmbralPublicKey
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.IntegerField(default=0)
    public_key = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'auth_profile'

    def __str__(self):
        return self.user.username+" "+str(self.account_type)+" "+str(self.public_key)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # user created. Create the sender for nu

        # teacher_dht_port = sys.argv[2]
        # teacher_rest_port = int(teacher_dht_port) + 100
        # with open("examples-runtime-cruft/node-metadata-{}".format(teacher_rest_port), "r") as f:
        #     f.seek(0)
        #     teacher_bytes = binascii.unhexlify(f.read())
        # URSULA = Ursula.from_bytes(teacher_bytes, federated_only=True)
        # print("Will learn from {}".format(URSULA))
        #





    instance.profile.save()
    print(instance.profile.account_type)


class Policy(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    public_key = models.CharField(max_length=500, null=True, blank=True)
    label = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Record(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    data = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class EncryptedRecord(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class PolicyUsers(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

