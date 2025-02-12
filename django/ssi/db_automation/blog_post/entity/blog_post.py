from django.db import models

from account_profile.entity.account_profile import AccountProfile


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    writer = models.ForeignKey(AccountProfile, on_delete=models.CASCADE, related_name="blog_posts")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog_post"
        app_label = "blog_post"
