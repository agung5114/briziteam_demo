# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Tweets(models.Model):
    index = models.IntegerField(primary_key=True)
    datetime = models.DateTimeField(db_column='Datetime', blank=True, null=True) 
    # datetime = models.TextField(db_column='Datetime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    keyword = models.TextField(db_column='Keyword', blank=True, null=True)  # Field name made lowercase.
    tweet_id = models.IntegerField(db_column='Tweet_Id', blank=True, null=True)  # Field name made lowercase.
    username = models.TextField(db_column='Username', blank=True, null=True)  # Field name made lowercase.
    likes = models.IntegerField(db_column='Likes', blank=True, null=True)  # Field name made lowercase.
    retweeted = models.IntegerField(db_column='Retweeted', blank=True, null=True)  # Field name made lowercase.
    text = models.TextField(db_column='Text', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    text_cleaned = models.TextField(db_column='Text_cleaned', blank=True, null=True)  # Field name made lowercase.
    sentiment = models.TextField(db_column='Sentiment', blank=True, null=True)  # Field name made lowercase.
    retrieved = models.IntegerField(db_column='Retrieved', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tweets'


class Retweets(models.Model):
    index = models.IntegerField(primary_key=True)
    datetime = models.TextField(db_column='Datetime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    keyword = models.TextField(db_column='Keyword', blank=True, null=True)  # Field name made lowercase.
    tweet_id = models.IntegerField(db_column='Tweet_Id', blank=True, null=True)  # Field name made lowercase.
    username = models.TextField(db_column='Username', blank=True, null=True)  # Field name made lowercase.
    retweeters = models.TextField(db_column='Retweeters', blank=True, null=True)  # Field name made lowercase.
    sentiment = models.TextField(db_column='Sentiment', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'retweets'


class Topdaily(models.Model):
    index = models.IntegerField(primary_key=True)
    indexkey = models.TextField(blank=True, null=True)
    retrieved = models.TextField(db_column='Retrieved', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    datetime = models.TextField(db_column='Datetime', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    keyword = models.TextField(db_column='Keyword', blank=True, null=True)  # Field name made lowercase.
    tweet_id = models.IntegerField(db_column='Tweet_Id', blank=True, null=True)  # Field name made lowercase.
    username = models.TextField(db_column='Username', blank=True, null=True)  # Field name made lowercase.
    likes = models.IntegerField(db_column='Likes', blank=True, null=True)  # Field name made lowercase.
    retweeted = models.IntegerField(db_column='Retweeted', blank=True, null=True)  # Field name made lowercase.
    text = models.TextField(db_column='Text', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    text_cleaned = models.TextField(db_column='Text_cleaned', blank=True, null=True)  # Field name made lowercase.
    sentiment = models.TextField(db_column='Sentiment', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'topdaily'
