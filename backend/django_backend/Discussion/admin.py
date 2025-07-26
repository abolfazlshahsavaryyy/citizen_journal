from django.contrib import admin
from Discussion.models.Discussion import Discussion
from Discussion.models.Topic import Topic
# Register your models here.
admin.site.register(Discussion)
admin.site.register(Topic)