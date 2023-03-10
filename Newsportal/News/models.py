from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from .sources import POSITIONS, article


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        author_articles_rating = Post.objects.filter(author=self).aggregate(post_rating=Sum('rating_post'))
        author_comments_rating = Comment.objects.filter(user_id=self.user).aggregate(com_rating=Sum('rating_comment'))
        all_comments_to_author_articles_rating = Comment.objects.filter(com_post__author__user=self.user).aggregate(
            comments_rating_sum=Sum('rating_comment'))
        self.user_rating = author_articles_rating['post_rating'] * 3 + author_comments_rating['com_rating'] + \
               all_comments_to_author_articles_rating['comments_rating_sum']
        self.save()



class Category(models.Model):
    name_category = models.CharField(unique=True, max_length=100)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=2,
                                 choices=POSITIONS,
                                 default=article)
    post_in = models.DateTimeField(auto_now_add=True)

    category = models.ManyToManyField(Category, through='PostCategory')
    post_header = models.CharField(max_length=255)
    post_text = models.TextField()
    rating_post = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)


    def like(self):
        self.rating_post += 1
        self.likes += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.dislikes -= 1

        self.save()

    def preview(self):
        return self.post_text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    com_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    com_text = models.TextField()
    com_in = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.likes += 1

        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.dislikes -= 1

        self.save()
