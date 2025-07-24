# myapp/models.py (Example content for a Django app's models.py file)
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

# Model 2: The "Many" side of the relationship (e.g., a news post on a page)
class News(models.Model):
    """
    Represents a news post, which belongs to a single Page.
    This is the 'many' side of the one-to-many relationship.
    """
    title = models.CharField(
        max_length=255, # Standardized max_length for titles
        help_text="The title of the news post."
    )
    text = models.TextField( # Changed to TextField for larger text content
        help_text="The full content of the news post."
    )
    like_count = models.IntegerField(
        default=0, # Default to 0 likes
        help_text="The number of likes this news post has received."
    )
    comment_count = models.IntegerField(
        default=0, # Default to 0 likes
        help_text="The number of comment this news post has received."
    )
    
    # ForeignKey field: This is the core of the one-to-many relationship.
    # - 'Page': Specifies the model this field relates to (the 'one' side).
    # - on_delete=models.CASCADE: If the associated Page is deleted, this News post will also be deleted.
    # - related_name='news_posts': This is the name used to access related News objects from a Page instance.
    #   For example, if you have a page object `my_page`, you can get all its news posts using `my_page.news_posts.all()`.
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='news_posts', # Renamed related_name for clarity (e.g., page.news_posts.all())
        help_text='Each news post must be associated with one page.'
        # null=False is the default for ForeignKey, so it's omitted for conciseness
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_news',
        blank=True,
        help_text='Users who liked this news post.'
    )
    
    published_date = models.DateTimeField(auto_now_add=True, help_text="The date and time the news post was published.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time the news post was last updated.")

    class Meta:
        verbose_name_plural = "News Posts" # Correct plural name for the admin interface
        ordering = ['-published_date'] # Order news posts by most recent first by default

    def __str__(self):
        """
        Returns a string representation of the News instance.
        """
        return f"News: {self.title} | Page: {self.page.name}"
    



