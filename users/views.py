from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
"""
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings"""

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} you can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

"""
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
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
        return super().form_valid(form)"""
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
