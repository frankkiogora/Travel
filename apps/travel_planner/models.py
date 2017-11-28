
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import date, datetime
from time import strptime
Name_Regex = re.compile(r'^[A-Za-z ]+$')

# Create your models here.
class userManager(models.Manager):
    def validate (self, postData):
        errors = []
        if len(User.objects.filter(username = postData['username'])) > 0:
            errors.append("Please travel a different name")
        if postData['password'] != postData['confirm_password']:
            errors.append("Password mismatch")
        if len(postData['name']) < 2:
            errors.append("Name needs to be more than 1 letter")
        if not Name_Regex.match(postData['name']):
            errors.append("name can only be letters")
        if len(postData['password']) < 8:
            errors.append("Password needs to be more than 8 letters")
        if len(errors) == 0:
            #create the user
            newuser = User.objects.create(name= postData['name'], username= postData['username'], password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            return (True, newuser)
        else:
            return (False, errors)

    def login(self, postData):
        errors = []
        if 'username' in postData and 'password' in postData:
            try:
              
                user = User.objects.get(username = postData['username'])
            except User.DoesNotExist: 
                
                errors.append("Try logging in again")
                return (False, errors)
      
        pw_match = bcrypt.hashpw(postData['password'].encode(), user.password.encode())
       
        if pw_match == user.password:
            return (True, user)
        else:
            errors.append("Loggin credentials incorrect !!")
            return (False, errors)


class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class travelManager(models.Manager):

    def travelval(self, postData, id):
        errors=[]
        if len(postData['destination']) < 1 :
            errors.append("Destination field cannot be blank")

        if len(postData['description']) < 1 :
            errors.append("You cannot leave a blank field")

        if str(date.today()) > str(postData['start']):
            errors.append("Please input a valid Date. .")

        if str(date.today()) > postData['end']:
            errors.append("Input date should be future")

        if postData['start'] > postData['end']:
            errors.append("Travel Date cannot be in future")
       
        if len(errors) == 0:
            plan= Travel.objects.create(destination=postData['destination'],description=postData['description'], start=postData['start'],end=postData['end'], creator= User.objects.get(id=id))
            
            return (True, plan)
        else:
           
            return (False, errors)

    def join(self, id, travel_id):
        
        if len(Travel.objects.filter(id=travel_id).filter(join__id=id))>0:
            return {'errors':'You already Joined this'}
        else:
            joiner= User.objects.get(id=id)
            plan= self.get(id= travel_id)
            plan.join.add(joiner)
            return {}


class Travel(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    start= models.DateField()
    end= models.DateField()
    creator= models.ForeignKey(User, related_name= "planner")
    join= models.ManyToManyField(User, related_name="joiner") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = travelManager()