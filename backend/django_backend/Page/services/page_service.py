from Page.models.Page import Page  # adjust import to your structure

def create_page(user, data):
    return Page.objects.create(
        user=user,
        name=data.get('name'),
        page_description=data.get('page_description'),
        post_count=0,
        follower_count=0,
        following_count=0
    )

def update_page(page: Page, validated_data: dict) -> Page:
    """
    Update a Page instance with validated data.
    """
    for attr, value in validated_data.items():
        setattr(page, attr, value)
    page.save()
    return page

def delete_page(page: Page) -> None:
    """
    Delete the given Page instance.
    """
    page.delete()