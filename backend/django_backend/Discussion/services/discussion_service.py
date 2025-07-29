# services/discussion_service.py
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from Discussion.models.Discussion import Discussion
from django.core.exceptions import ValidationError
from Page.models.Page import Page
def create_discussion(user, page_id, data):
    """
    Create a discussion for a page if not already exists and user owns the page.
    """
    page = get_object_or_404(Page, pk=page_id)

    # Check ownership
    if page.user != user:
        raise PermissionDenied("You do not have permission to create a discussion for this page.")

    # Check if page already has a discussion
    if hasattr(page, 'discussion'):
        raise ValidationError("This Page already has a Discussion configured.")

    # Create discussion (service does not validate serializer; that's done in view)
    discussion = Discussion.objects.create(
        page=page,
        name=data['name'],
        description=data['description'],
        is_active=data.get('is_active', True)  # default True if missing
    )
    return discussion
def update_discussion(user, discussion_id, data):
    """
    Update a discussion if the user owns the page.
    """
    discussion = get_object_or_404(Discussion, pk=discussion_id)

    # Permission check: must own the page
    if discussion.page.user != user:
        raise PermissionDenied("You do not have permission to edit this discussion.")

    for field, value in data.items():
        setattr(discussion, field, value)

    discussion.save()
    return discussion


def delete_discussion(user, discussion_id):
    """
    Delete a discussion if the user owns the page.
    """
    discussion = get_object_or_404(Discussion, pk=discussion_id)

    if discussion.page.user != user:
        raise PermissionDenied("You do not have permission to delete this discussion.")

    discussion.delete()
    return True

class DiscussionService:
    @staticmethod
    def get_user_discussions(user):
        # Fetch discussions where the page belongs to the user
        return Discussion.objects.select_related('page').filter(page__user=user)
