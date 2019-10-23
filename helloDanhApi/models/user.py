from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, firt_name, last_name, address, phone_number, password=None):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, firt_name, last_name, address, phone_number, password):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firt_name, last_name, address, phone_number, password):
        user = self.create_user(
            email,
            password=password,
            first_name="True",
            last_name="True",
            address=address,
            phone_number=phone_number,
        )

        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    phone_number = models.IntegerField()
    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name','last_name', 'address', 'phone_number' ]

    def __str__(self):              # __unicode__ on Python 2
        return self.email
