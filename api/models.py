from django.db import models
import os,string
from django.conf import settings
from datetime import *
from api.exceptions import Django2Exception
import django

class Images(models.Model):
    
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self,*args,**kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(Images,self).delete(*args,**kwargs)  

class Records(models.Model):

    def _get_upload_to(self, filename):
        return os.path.join(os.path.splitext(filename)[1][1:], filename)

    title = models.CharField(max_length=45,null=True)
    record = models.FileField(upload_to = _get_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self,*args,**kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.record.name))
        super(Records,self).delete(*args,**kwargs)  


class UserProfile(models.Model):
    ACTIVE = 'A'
    INACTIVE ='I'
    DELETED ='D'
    STATUS_CHOICES = ((ACTIVE, 'Active'), (INACTIVE, 'Inactive'),(DELETED, 'Deleted'))
    status = models.CharField(max_length=1,choices=STATUS_CHOICES, default=ACTIVE)
    name = models.CharField(max_length=45)
    display_name = models.CharField(max_length=45)
    upd_on = models.DateTimeField()
    mobile = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = True

    def create(self,data):
        
        ts = datetime.now()

        mandatoryfields = ('username','mobile','email','password','name')
        for field in mandatoryfields:
            if field not in data:
                raise Django2Exception(code = 4005,message='Field missing - {}'.format(field))
        
        if  django.contrib.auth.models.User.objects.filter(username=data['username']).exists():
            raise Django2Exception(code = 4005,message='Duplicate User Already exists - {0}'.format(data['username']))
    
        elif django.contrib.auth.models.User.objects.filter(email=data['email']).exists():
            raise Django2Exception(code = 4005,message='Duplicate User email Already exists - {0}'.format(data['email']))
        
        elif UserProfile.objects.filter(mobile=data['mobile']).exists():
            raise Django2Exception(code = 4005,message='Duplicate User email Already exists - {0}'.format(data['mobile']))

        else:
            auth_user = django.contrib.auth.models.User.objects.create_user(
                    username=data['username'],email=data['email'],first_name=data['name'])
            auth_user.set_password(data['password'])
        
            auth_user.is_active = 1
            auth_user.save()

            # Finally, save the userprofile
            self.user_id = auth_user.id
            self.display_name = auth_user.first_name
            self.name=self.get_name(auth_user.first_name)
            self.upd_on = ts
            self.mobile = data['mobile']
            self.save()
    
    def get_name(self,display_name):
        return ''.join(e.upper() for e in display_name if e.isalnum())
