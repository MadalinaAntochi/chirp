from django.contrib.auth.models import User
from django.db import models

# modelele --> clasele ce dau structura tabelelor

# tabela User se creaza automat

class TimestampModel(models.Model):
    class Meta:
        abstract=True
    created=models.DateTimeField(auto_now_add=True)


class Message(TimestampModel):
    user=models.ForeignKey(User)
    status=models.TextField(null=False, max_length=140, blank=False)

    # __str__ este toString-ul din Java
    def __str__(self):
        return self.status


class Like(TimestampModel):
    user=models.ForeignKey(User)
    message=models.ForeignKey(Message)
    like=models.BooleanField()

class Follow(TimestampModel):

    class meta:
        unique_together = [("followed_user", "following_user"),]

    followed_user=models.ForeignKey(User, related_name='followed_by')
    following_user=models.ForeignKey(User, related_name='following')

    def __str__(self):
        return "User {0} follows user {1}".format(self.following_user.username, self.followed_user.username)