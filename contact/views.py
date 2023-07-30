from django.shortcuts import render
from django.contrib import messages

from accounts.utils import send_contact_email, send_notification


# Create your views here.
def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        #send info notification
        mail_subject = "You have recieved a contact mail."
        mail_template = 'mail/contact_mail.html'
        
        context= {
            'to_email' :email,
            'name' : name,
            'subject' : subject,
            'message' : message,
        }
        send_contact_email(mail_subject, mail_template, context)
        print('email, done')

        messages.success(request, 'submitted successfully')

    return render(request, 'contact/contact.html')