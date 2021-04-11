"""Celery tasks."""

# Django
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Celery
from celery.decorators import task, periodic_task
from celery.task.schedules import crontab

# Models
from cassie.users.models import User

# Utilities
import jwt
from datetime import timedelta

def gen_verification_token(user):
  """Create JWT token that the user can use to verify its account."""
  exp_date = timezone.now() + timedelta(days=30)
  payload = {
    'user': user.username,
    'exp': int(exp_date.timestamp()),
    'type': 'email_confirmation'
  }
  token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
  return token

@task(name='send_cofirmation_email', max_retries=3)
def send_cofirmation_email(user_pk):
  """Send account verification link to given user."""
  user = User.objects.get(pk=user_pk)
  verification_token = gen_verification_token(user)

  subject = f'Welcome @{user.username}! Verify your account to start using Cassie'
  from_email = 'Cassie <noreply@cassie.com>'
  content = render_to_string(
    'emails/users/account_verification.html',
    { 'token': verification_token, 'user': user }
  )
  msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
  msg.attach_alternative(content, 'text/html')
  msg.send()

@periodic_task(name='delete_inactive_users', run_every=crontab(day_of_week=0))
def delete_inactive_users():
  """Delete all inactive user.

    An inactive user is a user doesn't confirm him
    account in 30 days. 
  """
  users = User.objects.filter(is_verified=False)
  for user in users:
    max_verification_date = user.created + timedelta(days=30)
    if max_verification_date > timezone.now():
      user.delete()
  # TODO: Send email saying why this account was deleted 