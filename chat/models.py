from django.db import models

# Spring user representation

class User(models.Model):
    alias = models.CharField(max_length=50, unique = True)
    email = models.EmailField(max_length=75, unique = True)
    admin_flag = models.BooleanField(default = False)
    friends = models.ManyToManyField("self",symmetrical=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    creation = models.DateField(auto_now_add=True)
    
    # consider having a file upload field for users?

    def __unicode__(self):
        return self.alias

    class Meta:
        verbose_name = "Spring user"

# chat model that has within it conversations

# Conversation

class Conversation(models.Model):
    members = models.ManyToManyField(User)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "chat conversation"

class Chat(models.Model):
    chat_text = models.CharField(max_length=250)
    from_user = models.ForeignKey(User)
    conversation = models.ForeignKey(Conversation)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.chat_text

    class Meta:
        verbose_name = "individual chat line"

class Query(models.Model):
    query_text = models.CharField(max_length=100)
    chats = models.ManyToManyField(Chat)
    users = models.ManyToManyField(User)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "query"







