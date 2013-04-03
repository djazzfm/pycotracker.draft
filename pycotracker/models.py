from django.db import models
from djazz.models import Config, ConfigManager
from djazz.posts.models import Post, PostManager,\
                               PostVar, PostVarManager


class TicketConfigManager(ConfigManager):
    def get_query_set(self):
        q = super(TicketConfigManager,self).get_query_set()
        return q.filter(section='pycotracker')

class TicketConfig(Config):
    objects = TicketConfigManager()
    class Meta:
        proxy = True


class TicketManager(PostManager):
    def get_query_set(self):
        q = super(TicketManager,self).get_query_set()
        return q.filter(type='ticket')

class Ticket(Post):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    
    TYPE = 'ticket'
    
    objects = TicketManager()
    class Meta:
        proxy = True


class TicketVarManager(PostVarManager):
    def get_query_set(self):
        q = super(TicketVarManager,self).get_query_set()
        return q.filter(post__type='ticket')

class TicketVar(PostVar):
    objects = TicketVarManager()
    class Meta:
        proxy = True


class TicketTagManager(PostVarManager):
    def get_query_set(self):
        q = super(TicketTagManager,self).get_query_set()
        return q.filter(post__type='ticket', key='tag')

class TicketTag(PostVar):
    objects = TicketTagManager()
    class Meta:
        proxy = True
    def save(self, *args, **kwargs):
        self.key = 'tag'
        return super(TicketTag, self).save(*args, **kwargs)

class TicketAssignementManager(PostVarManager):
    def get_query_set(self):
        q = super(TicketAssignementManager,self).get_query_set()
        return q.filter(post__type='ticket', key='assignement')

class TicketAssignement(PostVar):
    objects = TicketAssignementManager()
    class Meta:
        proxy = True
    def save(self, *args, **kwargs):
        self.key = 'assignement'
        return super(TicketAssignement, self).save(*args, **kwargs)
