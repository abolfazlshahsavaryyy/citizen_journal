from django.conf import settings
from django.db import models

# Model 1: The "One" side of the relationship (e.g., a social media page)
class Page(models.Model):
    """
    Represents a social media page.
    This is the 'one' side of the one-to-many relationship with News.
    """
    name = models.CharField(
        max_length=100,
        unique=True, # Ensure page names are unique
        help_text="The unique name of the page."
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post_count = models.IntegerField(
        default=0, # Default to 0 posts
        help_text="The total number of posts on this page."
    )
    follower_count = models.IntegerField(
        default=0, # Default to 0 followers
        help_text="The total number of followers for this page."
    )
    following_count = models.IntegerField(
        default=0, # Default to 0 following
        help_text="The total number of accounts this page is following."
    )
    page_description = models.TextField(
        max_length=1000, # Increased max_length for description
        blank=True, # Allow the field to be blank in forms/admin
        null=True, # Allow the field to be NULL in the database
        help_text="A detailed description of the page's content or purpose."
    )
    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followed_by', # This is the reverse relationship name
        blank=True, # Allow a page to follow no other pages
        help_text="Other pages that this page is following."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the page was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time the page was last updated.")

    class Meta:
        verbose_name_plural = "Pages" # Correct plural name for the admin interface
        ordering = ['follower_count'] # Order pages by name by default

    def __str__(self):
        """
        Returns a string representation of the Page instance.
        This is what will be displayed in the Django admin and other places.
        """
        return f"Page: {self.name} | Followers: {self.follower_count}"


