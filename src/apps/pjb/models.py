from django.db import models

class EdicaoPjb(models.Model):
    nome = models.TextField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'edição PJB'
        verbose_name_plural = 'edições PJB'


class ComissaoPjb(models.Model):
    edicao_pjb = models.ForeignKey(EdicaoPjb, on_delete=models.CASCADE)
    nome = models.TextField(null=True, blank=True)
    sigla = models.TextField(null=True, blank=True)
    presidente = models.ForeignKey('DeputadoPjb', null=True, blank=True, related_name='presidente', on_delete=models.CASCADE)
    vice_presidente = models.ForeignKey('DeputadoPjb', null=True, blank=True, related_name='vice_presidente', on_delete=models.CASCADE)
    integrantes = models.ManyToManyField('DeputadoPjb', blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'comissão PJB'
        verbose_name_plural = 'comissões PJB'

class DeputadoPjb(models.Model):
    edicao_pjb = models.ForeignKey(EdicaoPjb, on_delete=models.CASCADE)
    nome = models.TextField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    escola = models.TextField(null=True, blank=True)
    serie = models.TextField(null=True, blank=True)
    uf = models.TextField(null=True, blank=True)
    minibio = models.TextField(null=True, blank=True)
    foto = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'deputado PJB'
        verbose_name_plural = 'deputados PJB'

class ProjetoPjb(models.Model):
    edicao_pjb = models.ForeignKey(EdicaoPjb, on_delete=models.CASCADE)
    numero = models.TextField(help_text='Numeração completa')
    ementa = models.TextField(null=True, blank=True)
    entenda_a_proposta = models.TextField(null=True, blank=True)
    autor = models.ForeignKey('DeputadoPjb', related_name='autor', on_delete=models.CASCADE)
    comissoes = models.ManyToManyField('ComissaoPjb', blank=True)
    relator = models.ForeignKey('DeputadoPjb', null=True, blank=True, related_name='relator', on_delete=models.CASCADE)
    texto_original = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.numero

    class Meta:
        verbose_name = 'projeto PJB'
        verbose_name_plural = 'projetos PJB'


    
