# =================================================================== #
#                         COLEÇÃO DE IMPORTS                          #
# =================================================================== #
import time
from selenium.webdriver.common.by import By as by
from toolbox.library_tools.selenium_tools import check_type
from toolbox.library_tools.selenium_tools import select_type

# =================================================================== #
#                         DEFINIÇÕES DE CLASSE                        #
# =================================================================== #
class parcele_facil():
    def __init__(self, toolbox):
        self.toolbox = toolbox

# =================================================================== #
#                         CATÁLOGO DE FUNÇÕES                         #
# =================================================================== #
    def request_02(self):
    # Está função realiza o acesso ao front-unico e executa o a rotina de login

        # acessa a url do front-unico
        try: self.toolbox.selenium_webdriver.get(self.toolbox.selected_dictionary['features']['url'])
        except Exception as exception_error:
            self.toolbox.generate_report_execution(exception_error, optional_terminate_application = True)

        # insere as informações de login
        self.toolbox.selenium_write(by.ID, self.toolbox.selected_dictionary['object']['Usuario'], self.toolbox.selected_dictionary['data']['Usuario'])

        # insere as informações de senha
        self.toolbox.selenium_write(by.ID, self.toolbox.selected_dictionary['object']['Senha'], self.toolbox.selected_dictionary['data']['Senha'])

        # clica no check-box alterar
        self.toolbox.selenium_click(by.ID, self.toolbox.selected_dictionary['object']['Alterar'])

        # insere as informações de dominio
        self.toolbox.selenium_write(by.ID, self.toolbox.selected_dictionary['object']['Dominio'], self.toolbox.selected_dictionary['data']['Dominio'])

        # clica no botão entrar
        self.toolbox.selenium_click(by.ID, self.toolbox.selected_dictionary['object']['Entrar'])

        # seleciona a unidade
        self.toolbox.selenium_select(by.ID, self.toolbox.selected_dictionary['object']['Unidade'], select_type.select_item_by_text, self.toolbox.selected_dictionary['data']['Unidade'])

        # clica no botão avançar
        self.toolbox.selenium_click(by.ID, self.toolbox.selected_dictionary['object']['Avancar'])

        # valida o fluxo de login
        counter = 30
        while(counter > 0):
            try:
                # verifica se a pagina inicial foi carregada
                page_element = self.toolbox.check_element(by.ID, self.toolbox.selected_dictionary['object']['Validar_Login'], check_type.element_capture)
                page_element = (page_element.text).split('\n')

                # registra as evidencias
                if('Seja bem vindo' in str(page_element[0])):
                    self.toolbox.generate_report_execution('Url acessada: {}\nMensagem: {}'.format(self.toolbox.selected_dictionary['features']['url'], str(page_element[0])),
                                                           'servico\\tag_cen02_parcele_facil-request.txt',
                                                           'servico\\tag_cen02_parcele_facil-request.png')
                    return True

                else: return False

            except: counter = (counter - 1); time.sleep(1)

        if(counter == 0): self.toolbox.generate_report_execution('[ERRO] Não Foi possivel validar a realização do Login', optional_terminate_application = True)

    def comparison_02(self):
    # Esta função realiza a identificação do cliente e acessa a funcionalidade selecionada

        # clica no menu identificar cliente
        self.toolbox.selenium_click(by.ID, self.toolbox.selected_dictionary['object']['Identificar'])

        # insere as informações do cliente
        self.toolbox.selenium_write(by.ID, self.toolbox.selected_dictionary['object']['Cliente'], self.toolbox.selected_dictionary['data']['Cliente'])

        # clica no botão ok
        for page_element in self.toolbox.selenium_webdriver.find_elements(by.TAG_NAME, 'button'):
            try: 
                if(str(page_element.text) == 'OK'): page_element.click(); break
            except: pass

        # aguarda o término do processamento
        counter = 30
        while(counter > 0):
            try:
                if(self.toolbox.check_element(by.ID, self.toolbox.selected_dictionary['object']['Span_Identificar01'], check_type.element_check) == True
                or self.toolbox.check_element(by.ID, self.toolbox.selected_dictionary['object']['Span_Identificar02'], check_type.element_check) == True):
                    time.sleep(1); counter = (counter - 1)

                else: break

            except Exception as exception_error: 
                self.toolbox.generate_report_execution('[ERRO] Houve um erro ao tentar aguardar o processamento.\nDetalhes do Erro: {}'.format(exception_error), optional_terminate_application = True)

            finally:
                if(counter == 0):
                    self.toolbox.generate_report_execution('[ERRO] Não foi possivel concluir a identificação do cliente dentro do tempo limite.', optional_terminate_application = True)

        # navega no menu serviço
        self.toolbox.selenium_click(by.LINK_TEXT, self.toolbox.selected_dictionary['object']['Menu'].replace('Ã§', 'ç'))

        # navega no menu parcele facil
        self.toolbox.selenium_click(by.LINK_TEXT, self.toolbox.selected_dictionary['object']['Sub-Menu'].replace('Ã¡','á')) 

        # verifica se a funcionalidade foi acessada corretamente
        try:
            # verifica se a pagina incial foi carregada
            counter = 30
            while(counter > 0):
                try:
                    page_element = self.toolbox.check_element(by.ID, self.toolbox.selected_dictionary['object']['Formulario'], check_type.element_capture)
                    if(page_element.text != ''): page_element = (page_element.text).split('\n'); break
                except: counter = (counter - 1); time.sleep(1)

            if('Parcele Fácil' in page_element[0]):
                self.toolbox.generate_report_execution('Formulario acessado: {}'.format(str(page_element[0])),
                                                       'servico\\tag_cen02_parcele_facil-comparison.txt',
                                                       'servico\\tag_cen02_parcele_facil-comparison.png')
                return True

            else: return False
        except Exception as exception_error:
            self.toolbox.generate_report_execution(exception_error, optional_terminate_application = True)

    def validation_02(self):
    # Função responsável por realizar o fluxo da funcionalidade e encerrar o atendimento

        # cria a variavel que ira armazenar a resposta (sucesso ou falha) da automação
        validation = 'Falha'
        
        #Altera para saldo Parcial
        self.toolbox.selenium_select(by.ID, self.toolbox.selected_dictionary['object']['Saldo'], select_type.select_item_by_text, self.toolbox.selected_dictionary['data']['Saldo'])

        counter = 30
        while(counter > 0):
            try:
                page_element = self.toolbox.check_element(by.ID, self.toolbox.selected_dictionary['object']['Evidencia_saldo'], check_type.element_capture)
                self.toolbox.generate_report_execution('Informações Coletadas: {}'.format(page_element.text), 
                                                        'servico\\tag_cen02_parcele_facil-validation.txt',
                                                        'servico\\tag_cen02_parcele_facil-validation.png')

                validation = 'Sucesso'; counter = 0
            except: counter = (counter - 1); time.sleep(1)

        # clica no botão finalizar atendimento
        self.toolbox.selenium_click(by.ID, self.toolbox.selected_dictionary['object']['Finalizar'])

        # clica no botão sim do pop-up
        for page_element in self.toolbox.selenium_webdriver.find_elements(by.TAG_NAME, 'button'):
            try: 
                if(str(page_element.text) == 'Sim'): page_element.click(); break
            except: pass

        # clica no botão logoff
        self.toolbox.selenium_click(by.ID, self.toolbox.selected_dictionary['object']['Logoff'])

        # clica no botão sim do pop-up de confirmação
        self.toolbox.selenium_click(by.XPATH, self.toolbox.selected_dictionary['object']['Sim_Logoff'])

        # retorna o resultado da automação
        return validation