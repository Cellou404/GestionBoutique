from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages, auth

from .models import Profile
from .forms import UpdateProfileForm, UpdateProfilePictureForm


# Emailing
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            remember = request.POST['remember_me']
            if remember:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                settings.SESSION_EXPIRE_AFTER_LAST_ACTIVITY = False
        except:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
            settings.SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, f'🤝 Welcome back {user} 🤝')
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.error(request, 'Identifiants de connexion invalides')
            return redirect('/accounts/login/')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if first_name == '':
            messages.error(request, '😡 Le prénom doit être défini!')
            return redirect('register')

        if last_name == '':
            messages.error(request, '😡 Le nom doit être défini!')
            return redirect('register')

        if username == '':
            messages.error(request, '😡 Le nom d\'utilisateur doit être défini!')
            return redirect('register')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, '😡 Ce nom d\'utilisateur existe déjà. Veillez choisir un autre!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, '🙅 Addresse email existe déjà. Veillez choisir un autre!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    user.is_active = False
                    user.save()
                    messages.success(request, '👷 Compte créé avec succès 👏\n\nNous vous avons aussi envoyé un mail de confirmation afin d\'activer votre compte')
                    
                    # Welcome message
                    subject = "Activation de compte!"
                    message = f"Bonjour {user.username}! Bienvenue dans GB-SALIOU \n\nMerci d'activer votre compte.\nNous vous avons envoyé un email de vérification\nVeillez vérifier votre boite mail afin d'activer votre compte! \n\n\nThanking @admin"
                    from_mail = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    send_mail(subject, message, from_mail, to_list, fail_silently=False) 

                    # Email Address Confirmation
                    current_site = get_current_site(request)
                    email_subject = "Activation de compte @ GB-Saliou | Gestion de Boutique| Login"
                    message2 = render_to_string('accounts/email_confirmation.html',{
                        'name': user.username,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': generate_token.make_token(user)
                    })
                    send_mail(email_subject, message2, from_mail, to_list, fail_silently=False)
                    
                    return redirect('/accounts/login/')
                    
        else:
            messages.error(request, '👹 Les mots de passe ne correspondent pas!')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        messages.success(request, "Votre compte a été activé avec succès ✔✔✔")
        return redirect('/accounts/login/')
    else:
        return render(request, 'accounts/activation_failed.html')

def logout(request):
    auth.logout(request)
    messages.info(request, '😏 vous avez été déconnecté !')

    return redirect(reverse('login'))
    #return redirect('/accounts/login/')


def send_password_reset_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user is not None:
            # Generate and save the password reset token for the user
            token = generate_token.make_token(user)
            user.password_reset_token = token
            user.save()

            # Send the password reset email
            subject = 'Password Reset Request'
            message = f'Click the link to reset your password: {request.build_absolute_uri(reverse("password_reset_confirm", kwargs={"uidb64": urlsafe_base64_encode(force_bytes(user.pk)), "token": token}))}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

    return render(request, 'accounts/password_reset_request.html')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()
            return redirect('password_reset_done')

        return render(request, 'accounts/password_reset_confirm.html')
    else:
        return render(request, 'accounts/password_reset_invalid.html')


def profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    if request.method == 'POST':
        form = UpdateProfileForm(
            data=(request.POST or None),
            files=(request.FILES or None),
            instance=profile,
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profile d\'utilisateur a été mis à jour avec succès 👏')
            return HttpResponseRedirect('/accounts/profile/'+slug)
        else:
            messages.error(request, 'Quelque chose s\'est mal passé lors de la soumission du formulaire 😡')
            return HttpResponseRedirect('/accounts/profile/'+slug)
    else:
        form = UpdateProfileForm(instance=profile)
        context = {
            'profile': profile,
            'form': form
        }

        return render(request, 'accounts/profile.html', context)
