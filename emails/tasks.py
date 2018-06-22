import traceback

from django.conf import settings
from django.core.mail import send_mass_mail
from django.template import Template, Context
from django.urls import reverse
from django.core.mail import get_connection, EmailMultiAlternatives

from email_distribution_server.celery import app
from emails.submodels.email import Email
from emails.submodels.group_email import GroupEmail


class EmailsSender:
    def send_emails_by_group(self, group_emails_id, subject, body, sender_address):
        self._get_subscribe_emails_info_by_group(group_emails_id)
        self._create_emails_list(subject, body, sender_address)
        result = self._distribution_emails()
        return result

    def _get_subscribe_emails_info_by_group(self, group_emails_id):
        group_emails = GroupEmail.objects.get(id=group_emails_id)
        self._emails_info = Email.objects.filter(group=group_emails, subscription=True)
        # return emails_info

    def _create_emails_list(self, subject, body, sender_address):
        """
        Generate list with emails tuples
        :param emails_info: list Email objects
        :param subject:
        :param body: message in email
        :param sender_address:
        :return: list with tuples emails info
        """
        self._mails = []
        template_body = Template(body)
        for email in self._emails_info:
            context = Context({'unsubscribe_url': reverse('unsubscribe', kwargs={'hash': str(email.verification_hash)})})
            self._mails.append(
                (subject,
                 template_body.render(context),
                 template_body.render(context),
                 sender_address,
                 [email.email],
                 )
            )
        return self._mails

    def _distribution_emails(self):
        """
        Mass send emails
        :param emails:
        :return: Quantity success send emails
        """
        emails_tuple = tuple(self._mails)
        result = self._send_mass_html_mail(emails_tuple, fail_silently=False)
        return result

    def _send_mass_html_mail(self, datatuple, fail_silently=False, auth_user=None,
                   auth_password=None, connection=None):

        connection = connection or get_connection(
            username=auth_user,
            password=auth_password,
            fail_silently=fail_silently,
        )
        messages = []
        for subject, text, html, from_email, recipient in datatuple:
            message = EmailMultiAlternatives(subject, text, from_email, recipient)
            message.attach_alternative(html, 'text/html')
            messages.append(message)

        return connection.send_messages(messages)

    def get_all_select_emails_quantity(self):
        if hasattr(self, '_emails_info'):
            return self._emails_info.count()

        raise Exception('Attribute _emails_info not exist')


@app.task
def send_emails(*args, **kwargs):
    group_emails_id = kwargs.pop('group_emails', None)
    email_body = "Follow this link to unsubscribe: <a href='http://localhost:8000{{unsubscribe_url}}'>http://localhost:8000{{unsubscribe_url}}</a>"

    try:
        emails_sender = EmailsSender()
        quantity_sended_emails = emails_sender.send_emails_by_group(group_emails_id, 'Subject', email_body,
                                                                    settings.EMAIL_HOST_USER)
        quantity_total_emails = emails_sender.get_all_select_emails_quantity()
        print('All: %s, Sended: %s' % (quantity_total_emails, quantity_sended_emails))

    except:
        error = traceback.format_exc()
        print(error)
