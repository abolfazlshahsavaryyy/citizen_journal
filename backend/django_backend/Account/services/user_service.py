# Account/services/user_service.py

from Account.models.ApplicationUser import ApplicationUser
from Account.models.Profile import Profile
from Page.models.Page import Page
from django.db import transaction


@transaction.atomic
def register_user(*, username: str, email: str, password: str) -> ApplicationUser:
    """
    Creates a new ApplicationUser, Profile, and Page for registration.
    """
    user = ApplicationUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        role='citizen'  # fixed role
    )

    Profile.objects.create(user=user)

    Page.objects.create(
        name=f"{user.username}_page",
        user=user,
        page_description=f"{user.username}'s default page"
    )

    return user
