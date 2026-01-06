from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _



class CustomUserManager(UserManager):
    """ 
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email: str, password: str, first_name: str, last_name: str, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        if not first_name:
            raise ValueError(_('User must have first name'))
        if not last_name:
            raise ValueError(_('User must have last name'))
        

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, email: str, password: str, first_name: str, last_name: str, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        assert extra_fields['is_staff']
        assert extra_fields['is_superuser']
        return self.create_user(email, password, first_name, last_name, **extra_fields)