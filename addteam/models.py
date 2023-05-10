from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    mp = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    d = models.IntegerField(default=0)
    l = models.IntegerField(default=0)
    gf = models.IntegerField(default=0)
    ga = models.IntegerField(default=0)
    gd = models.IntegerField(default=0)
    pts = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Fixtures(models.Model):
    t1 = models.CharField(max_length=100)
    t2 = models.CharField(max_length=100)
    t1g = models.IntegerField(default = 0)
    t2g = models.IntegerField(default = 0)
    status = models.IntegerField(default = 0)

    def __str__(self):
        vs = self.t1+' vs '+self.t2
        return vs

    def vs(self):
        vs = self.t1+' vs '+self.t2
        return vs
