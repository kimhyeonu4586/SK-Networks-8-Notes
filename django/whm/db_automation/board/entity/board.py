from django.db import models
from django.utils.timezone import now

from account_profile.entity.account_profile import AccountProfile


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    writer = models.ForeignKey(
        AccountProfile,
        on_delete=models.CASCADE,
        related_name="boards",
        db_column="account_profile_id",
    )
    content = models.TextField(blank=False, null=False)
    create_date = models.DateTimeField(default=now, editable=False)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "board"
        app_label = "board"