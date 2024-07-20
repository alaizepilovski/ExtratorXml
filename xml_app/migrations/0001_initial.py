# Generated by Django 5.0.6 on 2024-07-20 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacidadeConsentimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=50)),
                ('city', models.CharField(default='', max_length=100)),
                ('accepted', models.BooleanField(default=False)),
                ('modificated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Privacidade e Consentimento',
                'verbose_name_plural': 'Privacidade e Consentimento',
                'db_table': 'xml_privacidade_consentimento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='XmlTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessao', models.CharField(max_length=1000)),
                ('chave', models.CharField(default='', max_length=44, unique=True)),
                ('xml', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Xml Temp',
                'verbose_name_plural': 'Xml Temps',
                'db_table': 'xml_xml_temp',
                'managed': True,
            },
        ),
    ]