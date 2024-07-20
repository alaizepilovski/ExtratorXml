from lxml import etree
from datetime import datetime


class Ler_XML():
    """
    Ler_XML(Arquivo XML é obrigatório) \n\n\n Abre o arquivo XML e extrai os valores de quase todas as Tags filhas do XML. \n\n\n
    * Tags Pai = [ide, emit, dest, autXML, det, total, transp, pag, infAdic] \n\n\n\n
    
    Funções (todas retornam um dict)\n\n
    
    * dados: Obtem informações da nota fiscal, número, data de emissão etc... \n
    * emitente: obtem informações do emitente, nome, cnpj etc... \n
    * produtos: informações dos produtos, são retornados em um dicionário com valores em lista {codi_pdi['1','2'],nome_pdi['produto1','produto2]}\n
    * outras_informacoes: somente informações adicionais do da nota
    """
    ...

    def __init__(self, xml):
        self.arquivo = xml
        self.ns = '{http://www.portalfiscal.inf.br/nfe}'
        
        # É criada uma representação em árvore do documento XML
        self.xml_tree = etree.fromstring(xml)

    def check_none(self,tag, typet='str'):
        """
        essa função é utilizada para verificar se um elemento XML é nulo ou não,
        e retornar um valor padrão caso seja nulo, para evitar erros de execução.
        A escolha entre retornar uma string vazia ou um float 0.00 depende do tipo esperado para o elemento.
        """

        tipo = typet
        if tag == None and tipo == 'str':
            return ""
        elif tag == None and tipo == 'int':
            return 0.00
        elif tag != None and tipo == 'int':
            return float(tag.text)
        else:
            return str(tag.text)

    @property
    def chave_nfe(self):
        try:
            protNFe_element = self.check_none(self.xml_tree.find(f'{self.ns}protNFe/{self.ns}infProt/{self.ns}chNFe'))
        except Exception as e:
            return None
        return protNFe_element
    
    @property
    def mod_nfe(self):
        try:
            ide_element = self.check_none(self.xml_tree.find(f'{self.ns}NFe/{self.ns}infNFe/{self.ns}ide/{self.ns}mod'))
        except Exception as e:
            return None
        return ide_element
    
    @property
    def uf_nfe(self):
        try:
            ide_element = self.check_none(self.xml_tree.find(f'{self.ns}NFe/{self.ns}infNFe/{self.ns}ide/{self.ns}cUF'))
        except Exception as e:
            return None
        return ide_element

    def dados_nfe(self, print_tags=False):
        """somente para verificar todas as tags existentes em 'ide'"""

        def tags_ide():
            """Apenas retornar todas as tags encontradas no xml no item IDE"""
            if print_tags == True:
                ide_element = self.xml_tree.find(f'{self.ns}NFe/{self.ns}infNFe/{self.ns}ide')
                tags_ide = []

                for child in ide_element:
                    tag = child.tag
                    tags_ide.append(tag.replace("{http://www.portalfiscal.inf.br/nfe}",""))
            else:
                tags_ide = []

            return tags_ide
            
        #percore vários elementos pais até encontrar a tag pai 'ide' desejada.
        ide_element = self.xml_tree.find(f'{self.ns}NFe/{self.ns}infNFe/{self.ns}ide')
        
        # pega cada tag filha abaixo das informações da NFe, porém adiconamos uma função para verificar se o elemento existe.
        natOpe_ide = self.check_none(ide_element.find(f'{self.ns}natOp'))
        mod_ide = self.check_none(ide_element.find(f'{self.ns}mod'))
        nNF_ide = self.check_none(ide_element.find(f'{self.ns}nNF'))
        dhEmi_ide = self.check_none(ide_element.find(f'{self.ns}dhEmi'))

        
        # Nota Referenciada, pode ser mais de uma
        NFRef_element  = self.xml_tree.findall(f'{self.ns}NFe/{self.ns}infNFe/{self.ns}ide/{self.ns}NFRef')

        NFRef_ide = []
        for i in NFRef_element:
            NFRef_ide.append(self.check_none(i.find(f'{self.ns}refNFe')))

        #coloca todas as informações em um dicionário
        
        dados = {
                'natOpe_ide': natOpe_ide,
                'mod_ide': mod_ide,
                'nNF_ide': nNF_ide,
                'dhEmi_ide': dhEmi_ide,
                'infAdic_ide': self.outras_informacoes()
                }
                
        return dados
    

    def produtos(self):
        """ Retorna uma lista com todos os produtos """
        #variavel para armazenar todos os dados dos produtos
        dados_pdi = []
        total_produtos = 0
        
        #busca todas as tags 'det' que se refere aos produtos no XML
        prod_element = self.xml_tree.findall(f'{self.ns}NFe/{self.ns}infNFe/{self.ns}det')

        #itera sobre cada produto encontrado e busca as informações
        for i in prod_element:

            #Salva os produtos na lista dentro do dicionário.
            pdi = {
            'cProd_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}cProd')),
            'xProd_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}xProd')),
            'NCM_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}NCM')),
            'CEST_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}CEST')),
            'CFOP_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}CFOP')),
            'uCom_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}uCom')),
            'qCom_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}qCom')),
            'vUnCom_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}vUnCom'),'int'),
            'vProd_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}vProd'),'int'),
            'vFrete_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}vFrete'),'int'),
            'vOutro_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}vOutro'),'int'),
            'vDesc_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}vDesc'),'int'),
            'vSeg_pdi':self.check_none(i.find(f'{self.ns}prod/{self.ns}vSeg'),'int'),
            'vIPI_pdi':self.check_none(i.find(f'{self.ns}imposto/{self.ns}IPI/{self.ns}IPITrib/{self.ns}vIPI'),'int')
            }
            
            dados_pdi.append(pdi)
            total_produtos += pdi['vProd_pdi']

        return dados_pdi, total_produtos
    
    def outras_informacoes(self):

        infAdic_element = self.check_none(self.xml_tree.find(f'{self.ns}NFe/{self.ns}infNFe/{self.ns}infAdic/{self.ns}infAdFisco'))

        return infAdic_element
    
    def emitente(self):
    
        #percore vários elementos pais até encontrar a tag pai emit desejada.
        emit_element = self.xml_tree.find(f'{self.ns}NFe/{self.ns}infNFe/{self.ns}emit')

        #pega cada tag filha abaixo das informaçoes do emitente, porém adiconamos uma função para verificar se o elemento existe.
        CNPJ_emit = self.check_none(emit_element.find(f'{self.ns}CNPJ'))
        if CNPJ_emit == '':
            CNPJ_emit = self.check_none(emit_element.find(f'{self.ns}CPF'))
        xNome_emit = self.check_none(emit_element.find(f'{self.ns}xNome'))
        xFant_emit = self.check_none(emit_element.find(f'{self.ns}xFant'))

        emitente = {
                    'CNPJ_emit':CNPJ_emit,
                    'xNome_emit':xNome_emit,
                    'xFant_emit':xFant_emit,
                    }

        return emitente