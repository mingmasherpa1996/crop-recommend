from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class User(models.Model):
      #p_id = models.IntegerField('p_id')
      first_name = models.CharField(max_length=200)
      last_name = models.CharField(max_length=200)
      gender = models.CharField(max_length=200)
      user_email = models.CharField(max_length=200)
      user_password = models.CharField(max_length=200)
      def __str__(self):
            return self.user_email