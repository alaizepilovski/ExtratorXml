from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
# Funções internas
from xml_app.extrator import Ler_XML
from xml_app.models import *
# libs de terceiros
from datetime import datetime
import pandas as pd
import uuid
import io


def real_br_money_mask(my_value):
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return f"R$ {c.replace('v','.')}"

def get_ip_and_city(request):
    """ 
        Extrai o IP e Cidade da pessoa que está usando a plataforma
        A fim de registrar o conhecimento dos termos.
        * Específico para hospedagem na vercel
    """
    ip_address = request.META.get('REMOTE_ADDR') # IP Do usuário
    ip_real = request.META.get('HTTP_X_FORWARDED_FOR') # IP Real
    ip = ''

    try:
        ip_real_split = str(ip_real).split(",")
        ip = ip_real_split[0]
        
    except Exception as e:
        ip = ip_real
        print(e)

    if ip_address and ip_real:
        return ip, ip_address
    else:
        return ip_address, ip

def clear_xmls():
    """ Caso algum XMl não seja excluido essa função limpará após uma hora"""

    now = timezone.now()
    xmls = XmlTemp.objects.all()
    if xmls:
        for xml in xmls:
            time = now - xml.created_at
            if time.seconds > 3600:
                xml.delete()

def home(request):

    return render(request, 'xml_app/home.html')

@csrf_exempt
def xml_termo_usuario(request):

    if request.method == 'POST':
        termo_aceito = False
        aceito = {'true': True,
                  'false': False}
        
        privacidade = aceito[request.POST.get('privacidade')]

        ip = get_ip_and_city(request)
        if privacidade:
            try:
                consentimento_existente = PrivacidadeConsentimento.objects.get(ip=ip[0])
                consentimento_existente.accepted = True
                consentimento_existente.city = ip[1] if ip[1] != None else ""
                consentimento_existente.save()
                termo_aceito = True
            except PrivacidadeConsentimento.DoesNotExist:
                novo_consentimento = PrivacidadeConsentimento()
                novo_consentimento.ip = ip[0]
                novo_consentimento.city = ip[1] if ip[1] != None else ""
                novo_consentimento.accepted = True
                novo_consentimento.save()
                termo_aceito = True
        else:
            try:
                consentimento_existente = PrivacidadeConsentimento.objects.get(ip=ip[0])
                consentimento_existente.accepted = False
                consentimento_existente.city = ip[1] if ip[1] != None else ""
                consentimento_existente.save()
            except PrivacidadeConsentimento.DoesNotExist:
                novo_consentimento = PrivacidadeConsentimento()
                novo_consentimento.ip = ip[0]
                novo_consentimento.city = ip[1] if ip[1] != None else ""
                novo_consentimento.accepted = False
                novo_consentimento.save()

        return JsonResponse({'aceito': termo_aceito})

def privacidade(request):

    return render(request, 'xml_app/privacidade.html')

def termos_condicoes(request):

    return render(request, 'xml_app/termos_condicoes.html')

def importar_xml(request):
    ip = get_ip_and_city(request)
    try:
        termo = PrivacidadeConsentimento.objects.get(ip=ip[0])
        if termo.accepted:
            termo_aceito = True
    except PrivacidadeConsentimento.DoesNotExist:
        termo_aceito = False

    response = render(request, 'xml_app/importar.html', {'termo_aceito': termo_aceito})

    session_xml = request.COOKIES.get('session_xml')
    if session_xml:
        try:
            XmlTemp.objects.get(sessao=session_xml).delete()
        except XmlTemp.DoesNotExist:
            ...

    response.delete_cookie('session_xml')

    return response

def tratar_xml(request):

    # Limpa os resquícios de xml que não foram excluidos, para nada ficar armazenado
    clear_xmls()

    if request.method == 'POST':
        xml = request.FILES['xml']
                
        try:
            xml_read = Ler_XML(xml.read())
            chave_nfe = xml_read.chave_nfe
        except Exception as e:
            context = {
                        'valid': False,
                        'msg': 'XML Inválido, por favor confira se realmente é um xml de NFe!',
                        }
            return render(request, 'xml_app/resultado.html', context)
        try:
            dados_nfe = xml_read.dados_nfe()
            produtos_nfe = xml_read.produtos()
            emitente_nfe = xml_read.emitente()

            for produto in produtos_nfe[0]:
                produto['vUnCom_pdi'] = real_br_money_mask(produto['vUnCom_pdi'])
                produto['vProd_pdi'] = real_br_money_mask(produto['vProd_pdi'])

            context = {
                'valid': True,
                'msg': f"Extração da NFe nº{dados_nfe['nNF_ide']}  realizada com sucesso!",
                'razao_emitente': emitente_nfe['xNome_emit'],
                'cnpj_emitente': emitente_nfe['CNPJ_emit'],
                'fantazia_emitente': emitente_nfe['xFant_emit'],
                'chave': chave_nfe,
                'emissao': datetime.fromisoformat(dados_nfe['dhEmi_ide'][0:10]),
                'produtos': produtos_nfe[0],
                'quantidade_produtos': len(produtos_nfe[0]),
                'total_produtos': real_br_money_mask(produtos_nfe[1]),
                'termo_aceito': True,
            }

            response = render(request, 'xml_app/resultado.html', context)

            try:
                session_exists = request.COOKIES.get('session_xml')
                if not session_exists:
                    sessao_key = uuid.uuid4()
                    response.set_cookie("session_xml", sessao_key)
                    session_xml = XmlTemp()
                    session_xml.sessao = sessao_key
                    session_xml.chave = chave_nfe
                    session_xml.xml = xml_read.produtos()
                    session_xml.save()
                else:
                    try:
                        session_xml = XmlTemp.objects.get(sessao=session_exists)
                    except XmlTemp.DoesNotExist:
                        sessao_key = uuid.uuid4()
                        response.set_cookie("session_xml", sessao_key)
                        session_xml = XmlTemp()
                        session_xml.sessao = sessao_key

                    session_xml.xml = xml_read.produtos()
                    session_xml.chave = chave_nfe
                    session_xml.save()

            except Exception as e:
                print(f'erro {e}')

            return response
        
        except Exception as e:
            context = {
                        'valid': False,
                        'termo_aceito': True,
                        'msg': f'XML Inválido, por favor confira se realmente é um xml de NFe! {e}',
                        }
            return render(request, 'xml_app/importar.html', context)

    return redirect('importar_xml')

def gerar_excel(request):

    session_exists = request.COOKIES.get('session_xml')
    if session_exists:
        try:
            xml = XmlTemp.objects.get(sessao=session_exists)
            dados_produtos = xml.get_produtos()

            try:
                df = pd.DataFrame(dados_produtos)
            except Exception as e:
                
                erro =  f"Uma falha ocorreu, por favor tente novamente ou entre em contato com o desenvolvedor do sistema, Aviso: Erro ao converter o dicionário para DataFrame: {e}"

            with io.BytesIO() as buffer:

                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:

                    df.to_excel(writer, sheet_name='Produtos', index=False)

                chave = int(xml.chave[25:34])
                filename = f'NFe - {chave} - relatorio_produtos_aksi.xlsx'
                response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename={filename}'
                xml.delete()

                return response
            
        except XmlTemp.DoesNotExist:
            erro = "Aviso: Por favor reimporte o xml para gerar um novo relatório"

        context = {
                    'valid': False,
                    'termo_aceito': True,
                    'msg': erro
                    }
        
        return render(request, 'xml_app/importar.html', context)

    return render(request, 'xml_app/importar.html', {'valid': True, 'msg':'Sem dados para geração do relatório', 'termo_aceito': True})