from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime
import time
today = datetime.date.today()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name_error'] = "Name must be 2 or more characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        if len(postData['password']) < 8 or len(postData['confirm_password']) < 8:
            errors['pass_length'] = "Password must be 8 or more characters"
        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = "Passwords must match"
        if User.objects.filter(email=postData['email']):
            errors['exists'] = "Email already taken"
        return errors
    
    def login(self, postData):
        errors = {}
        user_to_check = User.objects.filter(email=postData['email'])
        if len(user_to_check) > 0:
            user_to_check = user_to_check[0]
            if bcrypt.checkpw(postData['password'].encode(), user_to_check.password.encode()):
                user = {"user" : user_to_check}
                return user
            else:
                errors = { "error": "Login Invalid" }
                return errors
        else:
            errors = { "error": "Login Invalid" }
            return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
