from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
import random
import string
import uuid
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import UserProfile

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        # Генерация уникального токена
        token = uuid.uuid4().hex

        # Создайте или получите профиль пользователя
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.email_verification_token = token
        profile.save(update_fields=['email_verification_token'])

        # Формирование ссылки для подтверждения
        verification_link = self.request.build_absolute_uri(
            reverse_lazy('accounts:verify_email', kwargs={'token': token})
        )

        # Отправка письма с подтверждением
        send_mail(
            'Подтверждение регистрации',
            f'Пожалуйста, подтвердите ваш адрес электронной почты, перейдя по следующей ссылке: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return response

class VerifyEmailView(View):
    def get(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        User = get_user_model()

        try:
            user = User.objects.get(userprofile__email_verification_token=token)
            profile = user.userprofile
            profile.email_verified = True
            profile.email_verification_token = ''
            profile.save()
            return HttpResponse('Ваш email успешно подтвержден!')
        except User.DoesNotExist:
            return HttpResponse('Неверный или просроченный токен', status=400)
        
class PasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return super().form_valid(form)

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user.set_password(new_password)
        user.save()

        send_mail(
            'Восстановление пароля',
            f'Ваш новый пароль: {new_password}',
            'bogdanovskypro@yandex.ru',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class CustomLoginView(DjangoLoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('catalog:home')
