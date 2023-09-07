from django.db import models

# Create your models here.


class Pays(models.Model):
  nom_pays = models.CharField(max_length=200)
  drapeau = models.URLField()

class League(models.Model):
  id_league = models.IntegerField()
  nom_league = models.CharField(max_length=200)
  logo = models.URLField()
  types = models.CharField(max_length=200,null=True)
  pays = models.CharField(max_length=200)
  flags = models.URLField(null=True)
  annee = models.CharField(max_length=200)
  date_debut = models.CharField(max_length=200)
  date_fin = models.CharField(max_length=200)
  currently = models.BooleanField(default=False)

  