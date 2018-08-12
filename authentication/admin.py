from django.contrib import admin
from .models import Profile, Policy, Record, EncryptedRecord, PolicyUsers

admin.site.register(Profile)
admin.site.register(Policy)
admin.site.register(Record)
admin.site.register(EncryptedRecord)
admin.site.register(PolicyUsers)
