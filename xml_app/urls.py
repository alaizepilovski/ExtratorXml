from django.urls import path
from xml_app import views

urlpatterns = [
    path('', views.home, name='xml_home'),
    path('privacidade/', views.privacidade, name='xml_privacidade'),
    path('termos_condicoes/', views.termos_condicoes, name='xml_termos_condicoes'),
    path('importar_xml/', views.importar_xml, name='importar_xml'),
    path('tratar_xml/', views.tratar_xml, name='tratar_xml'),
    path('gerar_excel/', views.gerar_excel, name='gerar_excel'),
    path('termo/', views.xml_termo_usuario, name="xml_termo_usuario"),
]
