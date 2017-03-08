from __future__ import unicode_literals
from django.db import models
from ..login_registration.models import User

class MessageManager(models.Manager):
    def post_message(self, postData, written_to_id, written_by_id):
        errors = []
        if len(postData['message']) == 0:
            errors.append("Message cannot be blank!")
        if not errors:
            message = Message.objects.create(
                message=postData['message'],
                written_to=User.objects.get(id=written_to_id),
                written_by=User.objects.get(id=written_by_id)
            )
            print "Success!"
            return message
        else:
            print "Failure!"
            return errors

    def post_comment(self, postData, message_id, user_id):
        errors = []
        if len(postData['comment']) == 0:
            errors.append("Comment cannot be blank!")
        if not errors:
            comment = Comment.objects.create(
                comment=postData['comment'],
                message=Message.objects.get(id=message_id),
                user=User.objects.get(id=user_id)
            )
            print "Success!"
            return comment
        else:
            print "Failure!"
            return errors

class Message(models.Model):
    message = models.TextField(max_length=1000)
    written_to = models.ForeignKey(User)
    written_by = models.ForeignKey(User, related_name='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

    def __str__(self):
        return self.message

class Comment(models.Model):
    comment = models.TextField(max_length=1000)
    message = models.ForeignKey(Message)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
