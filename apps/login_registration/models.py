from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

# regex to test whether given name contains letters only and is no fewer than 2 characters
name_regex = re.compile(r'[A-Za-z]{2,}')
# regex to test whether given email is valid
email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-z]*$')
# regex to test whether given password is at least 8 characters long
password_regex = re.compile(r'(?=.{8,})')

class UserManager(models.Manager):
    def register(self, postData):
        # runs validation test
        errors = self.validate(postData)
        # creates a hashed password
        # sets user authority level
        # and stores user information into a new User object
        if not errors:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user_level = self.init_user_level()
            user = User.objects.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=hashed_password,
                user_level=user_level
            )
            print "Success!"
            return user
        else:
            print "Failure!"
            return errors

    # searches for Users matching the given email and tests whether the given
    # password matches the stored password
    def login(self, postData):
        user = User.objects.filter(email=postData['email'])
        if not user:
            return False
        if bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) != user[0].password.encode():
            return False
        else:
            return user[0]

    # deletes the session attached to the given user id
    def logout(self, session):
        del session
        return True

    # tests whether given user first name, last name, email, and password
    # are all valid
    def validate(self, postData):
        errors = []
        try:
            user = User.objects.get(email=postData['email'])
            errors.append("User email already exists! Please log in!")
        except:
            if not re.match(name_regex, postData['first_name']):
                errors.append("First name must be more than 2 characters!")
            if not re.match(name_regex, postData['last_name']):
                errors.append("Last name must be more than 2 characters!")
            if not re.match(email_regex, postData['email']):
                errors.append("Email address is invalid!")
            if not re.match(password_regex, postData['password']):
                errors.append("Password is invalid!")
            elif postData['password'] != postData['confirm_password']:
                errors.append("Passwords do not match!")
        return errors

    # sets the initial user level
    # first user registered is automatically made an admin
    # all following users are registered as normal users
    def init_user_level(self):
        users = User.objects.all()
        if len(users) == 0:
            return 9
        else:
            return 8

    # updates the given user's user level
    # only admins have access to this
    def set_user_level(self, postData):
        if postData['user_level'] == 8:
            return 8
        elif postData['user_level'] == 9:
            return 9

    # updates a given user's user information if user-inputted information is valid
    def update(self, postData, id, user_level):
        user = User.objects.get(id=id)
        if re.match(name_regex, postData['first_name']) and\
            len(postData['first_name']) != 0:
            user.first_name = postData['first_name']
        if re.match(name_regex, postData['last_name']) and\
            len(postData['last_name']) != 0:
            user.last_name = postData['last_name']
        if re.match(email_regex, postData['email']) and\
            len(postData['email']) != 0:
            user.email = postData['email']
        if len(postData['password']) != 0 and\
            re.match(password_regex, postData['password']) and\
            postData['password'] == postData['confirm_password']:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user.password = hashed_password
        if user_level == 9:
            user.user_level = int(postData['user_level'])
        if 'description' in postData:
            user.description = postData['description']
        user.save()

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
