from django.http import Http404
from django.shortcuts import render

from emails.submodels.email import Email


def unsubscribe(request, hash):
    try:
        email = Email.objects.get(verification_hash=hash)
    except Email.DoesNotExist:
        raise Http404("Email does not exist")

    email.subscription = False
    email.save()

    return render(request, 'unsubscribe.html')
