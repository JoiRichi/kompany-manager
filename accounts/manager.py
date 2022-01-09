from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    '''this will manage the class user'''
    def create_user(self, email, password = None):
        if not email:
            raise ValueError('Users must have a valid email address!')
        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('You must have a valid email Email!')
        user = self.create_user(email= self.normalize_email(email), password=password)

        user.is_staff = True
        user.is_superuser =True
        user.is_admin = True
        user.save(using= self._db)
        return user
