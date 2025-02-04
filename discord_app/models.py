from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin): 
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200,unique=True ,null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='user.png')

    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_by_natural_key(self, email):
        return self.__class__.objects.get(email=email)

    
    def has_perm(self, perm, obj=None):
        
        if self.is_superuser:
            return True
        return False

    def has_module_perms(self, app_label):
        
        if self.is_superuser or self.is_staff:
            return True
        return False


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User ,on_delete=models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic ,on_delete=models.SET_NULL, null = True)
    name = models.CharField(max_length=150)
    description= models.TextField(null = True,blank= True)
    participants = models.ManyToManyField(User, related_name='participants' ,blank=True)
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    room = models.ForeignKey(Room ,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]