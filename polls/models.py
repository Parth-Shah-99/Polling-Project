from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Question(models.Model):

    question_text = models.CharField(max_length=200)
    published_by = models.CharField(max_length=50)
    published_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text

    def __unicode__(self):
        return __str__(self)

    @property
    def total_votes(self):
        choices = self.choice_set.all()
        votes = 0
        for choice in choices:
            votes += choice.votes
        return votes

    @property
    def get_userobj(self):
        username = self.published_by
        user = User.objects.get(username=username)
        return user
    


class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def __unicode__(self):
        return __str__(self)

    @property
    def percentage_votes(self):
        percentage = (self.votes/self.question.total_votes)*100
        return float('%0.2f' % percentage)


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField('anonymous', default=False)
    profile_pic = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return __str__(self)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class UserVotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + self.choice.choice_text + " - " + self.question.question_text

    def __unicode__(self):
        return __str__(self)

    class Meta:
        verbose_name = 'User Vote'
        verbose_name_plural = 'User Votes'






