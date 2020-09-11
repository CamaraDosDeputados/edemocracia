from django.db import models

class DeputadoPjb(models.Model):
    nome = models.TextField()
    uf = models.TextField()

class ProjetoPjb(models.Model):
    deputado = models.ForeignKey(DeputadoPjb, on_delete=models.CASCADE)
    numero = models.TextField()
    nome = models.TextField()

    
