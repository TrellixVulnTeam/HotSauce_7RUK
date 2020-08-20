from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 3:
            errors["first_name"] = "First name should be at least 5 characters"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "Last name should be at least 5 characters"
            
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) < 6:
            errors["password"] = "Password should be at least 8 characters"
        if postData["password"] != postData["confirm_password"]:
            errors["confirm_password"] = "Password does not match"
        return errors

class User(models.Model): 
    first_name =  models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    email =  models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    img_url = models.CharField(max_length=200, null=True)
    price = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Purchase (models.Model):
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="purchases", on_delete=models.CASCADE)
    products = models.ForeignKey(Product, related_name="purchases", null=True, on_delete=models.CASCADE)
