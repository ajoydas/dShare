from django import forms
from django.contrib.auth.models import User

from authentication.models import Policy, Record


class PolicyForm(forms.Form):
    label = forms.CharField(label='Label')
    public_key = forms.CharField(label='Public Key')

    class Meta:
        model = Policy
        fields = ['label', 'public_key']


class RecordForm(forms.Form):
    policy = forms.IntegerField(label='Policy No.')
    data = forms.CharField(label='Data',
                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
                           max_length=300,
                           )

    class Meta:
        model = Record
        fields = ['policy', 'data']
