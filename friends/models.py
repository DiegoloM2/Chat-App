from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from chat.models import Message, Thread


# Create your models here.

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name = 'friends', default = None)

    def __str__(self):
        return self.user.username + "'s friendlist"

    def add_friend(self, account):
        """
        Add a new friend
        """

        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
        
    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        self.remove_friend(removee)
        removeeFriendList = FriendList.objects.get(user = removee)
        removeeFriendList.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "receiver")

    is_active = models.BooleanField(blank = True, null = False, default = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Accept friend request
        Upddate both sender and receiver friendlist
        """

        self.is_active = False
        self.save()

        senderFriendList = FriendList.objects.get(user = self.sender)
        receiverFriendList = FriendList.objects.get(user = self.receiver)

        senderFriendList.add_friend(self.receiver)
        receiverFriendList.add_friend(self.sender)
        
        thread = Thread.objects.get_or_create_personal_thread(self.sender, self.receiver)
        m = Message(sender = self.sender, thread = thread, text = "We are now friends! (Message from Mectio)")
        print(m)
        m.save()

        self.removeEqualOppositeRequest()

    def decline(self):
        """
        Decline a friend
        """
        self.is_active = False
        self.save()
        self.removeEqualOppositeRequest()
    
    def cancel(self):
        self.is_active = False
        self.save()

    def removeEqualOppositeRequest(self):
        print("hello")
        try:
            fRequest = FriendRequest.objects.get(sender = self.receiver, receiver = self.sender)
            fRequest.is_active = False
            frequest.save()
        except ObjectDoesNotExist:
            print("does not exist")
