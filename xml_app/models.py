from django.db import models
import ast


class XmlTemp(models.Model):
    sessao = models.CharField(max_length=1000)
    chave = models.CharField(max_length=44, default="", unique=True)
    xml = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'xml_xml_temp'
        managed = True
        verbose_name = 'Xml Temp'
        verbose_name_plural = 'Xml Temps'

    def __str__(self) -> str:
        return f"{self.created_at}"
    
    def get_produtos(self):
        return ast.literal_eval(self.xml)[0]


class PrivacidadeConsentimento(models.Model):
    ip = models.CharField(max_length=50)
    city = models.CharField(max_length=100, default='')
    accepted = models.BooleanField(default=False)
    modificated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'xml_privacidade_consentimento'
        managed = True
        verbose_name = 'Privacidade e Consentimento'
        verbose_name_plural = 'Privacidade e Consentimento'

    def __str__(self) -> str:
        return self.ip
