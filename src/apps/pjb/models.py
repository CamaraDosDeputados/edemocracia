from django.db import models
from datetime import datetime


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
    presidente = models.ForeignKey('DeputadoPjb', null=True, blank=True,
                                   related_name='%(class)s_presidente',
                                   on_delete=models.CASCADE)
    vice_presidente = models.ForeignKey('DeputadoPjb', null=True, blank=True,
                                        related_name='%(class)s_vice_presidente',
                                        on_delete=models.CASCADE)
    integrantes = models.ManyToManyField('DeputadoPjb', blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'comissão PJB'
        verbose_name_plural = 'comissões PJB'

class MesaDiretoraPjb(models.Model):
    edicao_pjb = models.ForeignKey(EdicaoPjb, on_delete=models.CASCADE)
    presidente = models.ForeignKey('DeputadoPjb', null=True, blank=True,
                                   related_name='%(class)s_presidente',
                                   on_delete=models.CASCADE)
    vice_presidente = models.ForeignKey('DeputadoPjb', null=True, blank=True,
                                        related_name='%(class)s_vice_presidente',
                                        on_delete=models.CASCADE)
    primeiro_secretario = models.ForeignKey('DeputadoPjb', null=True, blank=True,
                                        related_name='%(class)s_primeiro_secretario',
                                        on_delete=models.CASCADE)
    segundo_secretario = models.ForeignKey('DeputadoPjb', null=True, blank=True,
                                        related_name='%(class)s_segundo_secretario',
                                        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'mesa diretora PJB'
        verbose_name_plural = 'mesas diretoras PJB'

class PartidoPjb(models.Model):
    edicao_pjb = models.ForeignKey(EdicaoPjb, on_delete=models.CASCADE)
    nome = models.TextField(null=True, blank=True)
    sigla = models.TextField(null=True, blank=True)
    lider = models.ForeignKey('DeputadoPjb', null=True, blank=True,
                                   related_name='%(class)s_lider',
                                   on_delete=models.CASCADE)
    vice_lider = models.ForeignKey('DeputadoPjb', null=True, blank=True,
                                        related_name='%(class)s_vice_lider',
                                        on_delete=models.CASCADE)
    integrantes = models.ManyToManyField('DeputadoPjb', blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'partido PJB'
        verbose_name_plural = 'partidos PJB'

class DeputadoPjb(models.Model):
    edicao_pjb = models.ForeignKey(EdicaoPjb, on_delete=models.CASCADE)
    nome = models.TextField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    escola = models.TextField(null=True, blank=True)
    serie = models.TextField(null=True, blank=True)
    uf = models.TextField(null=True, blank=True)
    minibio = models.TextField(null=True, blank=True)
    foto = models.ImageField(upload_to="deputado_pjb_foto/", null=True,
                             blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'deputado PJB'
        verbose_name_plural = 'deputados PJB'

    @property
    def idade(self):
        if not self.data_nascimento:
            return 0
        delta = datetime.now().date() - self.data_nascimento
        return int(delta.days / 365.25)


class ProjetoPjb(models.Model):
    STATUS_PROJETO_CHOICES = [
        ('AAC', 'Aguardando apreciação na comissão'),
        ('APC', 'Aprovado em caráter conclusivo na comissão'),
        ('RJ', 'Rejeitado'),
        ('EPF', 'Encaminhado para plenária final'),
        ('APF', 'Aprovado na plenária final'),
        ('ADS', 'Aguardando designação de status'),
    ]


    edicao_pjb = models.ForeignKey(EdicaoPjb, on_delete=models.CASCADE)
    sigla_tipo = models.CharField(max_length=3)
    numero = models.CharField(max_length=4)
    ano = models.IntegerField()
    ementa = models.TextField(null=True, blank=True)
    entenda_a_proposta = models.TextField(null=True, blank=True)
    autor = models.ForeignKey('DeputadoPjb', related_name='autor',
                              on_delete=models.CASCADE)
    comissoes = models.ManyToManyField('ComissaoPjb', blank=True)
    relator = models.ForeignKey('DeputadoPjb', null=True, blank=True,
                                related_name='relator',
                                on_delete=models.CASCADE)
    texto_original = models.FileField(upload_to="projeto_pjb/", null=True,
                                      blank=True)
    parecer = models.FileField(upload_to="parecer/", null=True,
                                      blank=True)
    situacao = models.CharField(
        max_length=3,
        choices=STATUS_PROJETO_CHOICES,
        default='ADS',
    )

    def epigrafe(self):
        return str(self)

    def __str__(self):
        return '{} {}/{}'.format(self.sigla_tipo, self.numero, self.ano)

    class Meta:
        verbose_name = 'projeto PJB'
        verbose_name_plural = 'projetos PJB'
