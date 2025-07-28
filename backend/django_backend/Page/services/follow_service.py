# services/follow_service.py
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from Page.models.Page import Page

def toggle_follow(follower_page_id: int, target_page_id: int, user):
    """
    Toggle follow/unfollow between two pages.
    Returns: (action, follower_page, target_page)
    """
    if follower_page_id == target_page_id:
        raise ValueError("A page cannot follow itself.")

    # Get follower page (ownership check)
    try:
        follower_page = Page.objects.get(id=follower_page_id, user=user)
    except Page.DoesNotExist:
        raise PermissionDenied("You do not own this follower page.")

    # Get target page
    try:
        target_page = Page.objects.get(id=target_page_id)
    except Page.DoesNotExist:
        raise ObjectDoesNotExist("Target page does not exist.")

    # Toggle logic
    if target_page in follower_page.follows.all():
        # Unfollow
        follower_page.follows.remove(target_page)
        follower_page.following_count = max(0, follower_page.following_count - 1)
        target_page.follower_count = max(0, target_page.follower_count - 1)
        action = "unfollowed"
        message = f"{follower_page.name} has unfollowed {target_page.name}."
    else:
        # Follow
        follower_page.follows.add(target_page)
        follower_page.following_count += 1
        target_page.follower_count += 1
        action = "followed"
        message = f"{follower_page.name} now follows {target_page.name}."

    # Save both
    follower_page.save(update_fields=["following_count"])
    target_page.save(update_fields=["follower_count"])

    return action, message, follower_page, target_page
