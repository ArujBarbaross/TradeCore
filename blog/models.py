from django.db import models
from django.conf import settings
from django.dispatch import receiver



# this part was supposed to be used with clearbit enrichment, but alas
class BlogUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='blog_profile')
    enriched = models.BooleanField(verbose_name="Am I rich?", default=False)
    
    def _username(self):
        return self.user.username
    username = property(_username)

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(BlogUserProfile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=80)
    text = models.TextField()
    likes = models.ManyToManyField(BlogUserProfile, related_name='likes')


# the recivers probably should be put somewhere else
@receiver(models.signals.post_save, sender=BlogUserProfile)
def enrich(sender, instance, created, **kwargs):
    if created:
        # here be request to get rich data
        instance.enriched = True
        instance.save()


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_blog_user(sender, instance, created, **kwargs):
    if created:
        BlogUserProfile.objects.create(user=instance)
        instance.active = True
        instance.save()