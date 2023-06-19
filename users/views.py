from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template import loader
from django.shortcuts import render
from django.views import View




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Email verification
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message=render_to_string('users/account_activation_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            )
            email = EmailMessage(mail_subject,
                                message,
                                settings.EMAIL_HOST_USER,
                                [form.cleaned_data['email']]
                                )
            
            email.send()

            return redirect('account_activation_sent')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages = 'Account was successfully created'
            return redirect('login')
        return render(request, 'users/activate_failed.html', status=401)




class CustomPasswordResetView( PasswordResetView):
    def form_valid(self, form):
        try:
            # Get the currently logged-in user
            user = self.request.user

            # Generate the token
            token = default_token_generator.make_token(user)

            # Build the reset password URL
            reset_url = self.request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': user.pk, 'token': token}))

            # Compose the email content
            email_subject = 'Reset your password'
            email_message = f'Please click the following link to reset your password: {reset_url}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            # Send the email
            send_mail(email_subject, email_message, from_email, recipient_list)

            messages.success(self.request, 'Password reset email has been sent. Please check your email.')
            return super().form_valid(form)
        except AttributeError:
            messages.warning(self.request, 'Your email is not in our system.')
            return super().form_invalid(form)


@login_required()
def profile(request):
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            profile = p_form.save(commit=False)
            profile.bio = p_form.cleaned_data['bio']
            profile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)
