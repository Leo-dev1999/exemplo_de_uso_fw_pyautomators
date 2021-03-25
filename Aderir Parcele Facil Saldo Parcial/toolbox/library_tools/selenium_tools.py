# =================================================================== #
#                         DESCRIÇÃO DO ARQUIVO                        #
# =================================================================== #
# Descrição: Conjunto de funcionalidades desenvolvidas para           #
#            facilitar o uso dos comandos e funcionalidades do        #
#            Selenium, incluindo tratamentos e recursividades úteis   #
#            que otimizam a execução e programação do código.         #
# Empresa: Indra Company (www.indracompany.com)                       #
# Desenvolvedor: Douglas da Silva Garcia / Leonardo R. Evangelista    #
# Atualização: 14 / Novembro / 2019                                   #
# =================================================================== #

# =================================================================== #
#                         COLEÇÃO DE IMPORTS                          #
# =================================================================== #
import os
import time
import selenium
from enum import Enum
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# =================================================================== #
#                         DEFINIÇÕES DE CLASSE                        #
# =================================================================== #
class select_type(Enum):
# classe criada para uso como parâmetro na função selenium_select
    select_item_by_text = 'text'
    select_item_by_value = 'value'
    select_item_by_index = 'index'

class check_type(Enum):
# classe criada para uso como parâmetro na função check_element
    element_wait = 'wait'
    element_check = 'check'
    element_capture = 'capture'
    element_enabled = 'enabled'
    element_displayed = 'displayed'

class selenium_tools():
    def __init__(self, selenium_webdriver, optional_config = None):
    
        # realiza a contrução e configuração do selenium webdriver
        self.selenium_webdriver = self.driver_build(selenium_webdriver, optional_config)
        if(optional_config is None): self.driver_config()

# =================================================================== #
#                         CATÁLOGO DE FUNÇÕES                         #
# =================================================================== #

    def import_webdriver(self):
    # Função que retorna o driver do selenium para o método que realizou a sua chamada.
        return self.selenium_webdriver

    def driver_build(self, selenium_webdriver, optional_config = None):
    # Função responsável por montar o driver do selenium que será utilizado na automação

        # configura o browser escolhido e retorna o objeto contendo o webdriver
        try:

            # montagem do driver chromedriver
            if(selenium_webdriver == 'google chrome'):

                # realiza os imports exclusivos do navegador
                from webdriver_manager.chrome import ChromeDriverManager

                # configura o path onde será baixado o chromedriver
                path = ('{}/driver/chromedriver.exe'.format(os.getcwd()))

                # executa o webdriver
                if(optional_config == None):
                    webdriver = selenium.webdriver.Chrome(ChromeDriverManager(path=path).install())
                else:
                    webdriver = selenium.webdriver.Chrome(ChromeDriverManager(path=path).install(), chrome_options=optional_config)

            # montagem do driver geckodriver
            elif(selenium_webdriver == 'mozilla firefox'):

                # realiza os imports exclusivos do navegador
                from webdriver_manager.firefox import GeckoDriverManager

                # configura o binário do driver e o path onde será baixado o geckodriver
                path = ('{}/driver/geckodriver.exe'.format(os.getcwd()))
                binary = ('C:/Program Files/Mozilla Firefox/firefox.exe')

                # executa o webdriver
                if(optional_config == None):
                    webdriver = selenium.webdriver.Firefox(executable_path = GeckoDriverManager(path=path).install(), firefox_binary=binary)
                else:
                    webdriver = selenium.webdriver.Firefox(executable_path = GeckoDriverManager(path=path).install(), firefox_binary=binary, firefox_options=optional_config)

            # montagem do driver MicrosoftWebDriver      
            elif(selenium_webdriver == 'microsoft edge'):

                # configura o path onde está o executável
                path = './driver/MicrosoftWebDriver.exe'

                # executa o webdriver
                webdriver = selenium.webdriver.Edge(path)

            # montagem do driver IEDriverServer
            elif(selenium_webdriver == 'internet explorer'):

                # realiza os imports exclusivos do navegador
                from selenium.webdriver.ie.options import Options

                # define as configurações adicionais do driver
                if(optional_config == None): optional_config = Options()
                optional_config.ignore_protected_mode_settings = True

                # configura o path onde será executado o driver
                path = ('./driver/IEDriverServer.exe')

                # executa o webdriver
                webdriver = selenium.webdriver.Ie(executable_path=path, options=optional_config)

            else:
                raise Exception('[ERRO] Não foi informado um webdriver válido!')

        except Exception as exception_error:
            raise Exception('[ERRO] Não foi possivel construir o driver do selenium.\nDetalhes do erro: {}'.format(exception_error))

        # retorna o objeto contendo o webdriver do selenium
        return webdriver

    def driver_config(self):
    # função que realiza a configuração do webdriver do selenium

        try:
            # maximiza a janela do navegador
            self.selenium_webdriver.maximize_window()

            # deleta todos os cookies antes de começar a sessão
            self.selenium_webdriver.delete_all_cookies()

            # define o tempo limite para a automação encontrar algum elemento
            self.selenium_webdriver.implicitly_wait(1)

            # define o tempo limite para a página carregar
            self.selenium_webdriver.set_page_load_timeout(60)

            # define o tempo limite de tolerancia para a execução de algum script
            self.selenium_webdriver.set_script_timeout(30)

        except Exception as exception_error:
            self.global_tools.generate_report_execution(exception_error, optional_terminate_application=True)

        return True

    def check_element(self, by, element, check_type, optional_by = None, 
                      optional_element = None, optional_attempts = 30):
    # Função que analisa um determinado elemento e retorna o seu status

        # definição das variáveis
        page_element = None

        # procura o elemento na página com base nos parâmetros informados
        try:
            if(optional_by != None and optional_element != None):
                page_element = self.selenium_webdriver.find_element(optional_by, optional_element)
                page_element = page_element.find_element(by, element)

            else: page_element = self.selenium_webdriver.find_element(by, element)

        except: return False

        # retorna o elemento capturado
        if(check_type.value == 'capture'): return page_element

        # verifica se o elemento está habilitado
        elif(check_type.value == 'enabled'):
            if(page_element.is_enabled() == True): return True
            else: return False

        # verifica se o elemento está visível
        elif(check_type.value == 'displayed'):
            if(page_element.is_displayed() == True): return True
            else: return False

        # verifica se o elemento existe na página
        elif(check_type.value == 'check'):

            # move o cursor até o elemento
            try:
                self.selenium_webdriver.execute_script("arguments[0].scrollIntoView(true);", page_element)
                self.action_chains.move_to_element(page_element).perform()

            except: pass

            # verifica se o elemento está disponível para interação
            if(page_element.is_displayed() == True and page_element.is_enabled() == True): return True
            else: return False

        # espera o elemento estar pronto para interagir
        elif(check_type.value == 'wait'):
            while(optional_attempts > 0):
                
                # move o cursor até o elemento
                try:
                    self.selenium_webdriver.execute_script("arguments[0].scrollIntoView(true);", page_element)
                    self.action_chains.move_to_element(page_element).perform()

                except: pass

                # verifica se o elemento está disponível para interação
                if(page_element.is_displayed() == True and page_element.is_enabled() == True): return True
                else: optional_attempts = (optional_attempts - 1)
            
            return False

        else: raise Exception('Não foi informado um modo de verificação válido')

    def selenium_click(self, by, element, optional_by = None, optional_element = None,
                       optional_attempts = 30, optional_terminate_application = True):
    # Função que clica em um determinado objeto da página

        # definição das variáveis
        page_element = None
        execution_error = ''

        # realiza um determinado numero de tentativas de realizar a interação
        while(optional_attempts > 0):

            try:
                # procura o elemento na página com base nos parâmetros informados
                if(optional_by != None and optional_element != None):
                    page_element = self.selenium_webdriver.find_element(optional_by, optional_element)
                    page_element = page_element.find_element(by, element)

                else: page_element = self.selenium_webdriver.find_element(by, element)

                # verifica se o elemento está visível e habilitado para interação
                if(page_element.is_displayed() == True and page_element.is_enabled() == True):

                    # move o cursor até o elemento
                    try:
                        self.selenium_webdriver.execute_script("arguments[0].scrollIntoView(true);", page_element)
                        self.action_chains.move_to_element(page_element).perform()

                    except: pass

                    # realiza a interação com o elemento
                    page_element.click()
                    break

                else:
                    execution_error = '[ERRO] Element is not displayed or enabled'
                    optional_attempts = (optional_attempts - 1)

            except Exception as exception_error:
            # registra o erro ocorrido e diminui o contador de tentativas
                time.sleep(1)
                execution_error = exception_error
                optional_attempts = (optional_attempts - 1)

        # gera o relatório de erros e para a execução (caso a intereção não tenha sido realizada)
        if(optional_attempts == 0):
            execution_error = ('[Detalhes do Erro]: {}\n[Elemento]: By.{} "{}"'.format(execution_error, by, element))

            if(optional_by != None and optional_element != None): 
                execution_error = ('{}\n[Elemento Opcional]: By.{} "{}"'.format(execution_error, optional_by, optional_element))

            self.global_tools.generate_report_execution(execution_error, optional_terminate_application=optional_terminate_application)

        else: return True

    def selenium_write(self, by, element, text, optional_by = None, optional_element = None,
                       optional_attempts = 30, optional_terminate_application = True):
    # Função que digita o texto informado em um determinado objeto na página

        # definição das variáveis
        page_element = None
        execution_error = ''

        # realiza um determinado número de tentativas de realizar a interação
        while(optional_attempts > 0):

            try:
                # procura o elemento na página com base nos parâmetros informados
                if(optional_by != None and optional_element != None):
                    page_element = self.selenium_webdriver.find_element(optional_by, optional_element)
                    page_element = page_element.find_element(by, element)

                else: page_element = self.selenium_webdriver.find_element(by, element)

                # verifica se o elemento está visível e habilitado para interação
                if(page_element.is_displayed() == True and page_element.is_enabled() == True):

                    # realiza a interação com o elemento
                    page_element.clear()
                    page_element.send_keys(text.strip())
                    break

                else:
                    execution_error = '[ERRO] Element is not displayed or enabled'
                    optional_attempts = (optional_attempts - 1)

            except Exception as exception_error:
            # registra o erro ocorrido e diminui o contador de tentativas
                time.sleep(1)
                execution_error = exception_error
                optional_attempts = (optional_attempts - 1)

        # gera o relatório de erros e para a execução (caso a intereção não tenha sido realizada)
        if(optional_attempts == 0):
            execution_error = ('[Detalhes do Erro]: {}\n[Elemento]: By.{} "{}"'.format(execution_error, by, element))

            if(optional_by != None and optional_element != None): 
                execution_error = ('{}\n[Elemento Opcional]: By.{} "{}"'.format(execution_error, optional_by, optional_element))

            self.global_tools.generate_report_execution(execution_error, optional_terminate_application=optional_terminate_application)

        else: return True

    def selenium_select(self, by, element, select_type, select_options, optional_by = None, 
                        optional_element = None, optional_attempts = 30, optional_terminate_application = True):
    # Função que seleciona o elemento informado em um determinado objeto da página

        # definição das variáveis
        page_element = None
        execution_error = ''

        # realiza um determinado número de tentativas de realizar a interação
        while(optional_attempts > 0):

            try:
                # procura o elemento na página com base nos parâmetros informados
                if(optional_by != None and optional_element != None):
                    page_element = self.selenium_webdriver.find_element(optional_by, optional_element)
                    page_element = page_element.find_element(by, element)

                else: page_element = self.selenium_webdriver.find_element(by, element)

                # verifica se o elemento está visível e habilitado para interação
                if(page_element.is_displayed() == True and page_element.is_enabled() == True):

                    # seleciona o elemento a partir do valor
                    if(select_type.value == 'value'): Select(page_element).select_by_value(page_element); break

                    # seleciona o elemento a partir do índice
                    elif(select_type.value == 'index'): Select(page_element).select_by_index(page_element); break

                    # seleciona o elemento a partir do texto
                    elif(select_type.value == 'text'): Select(page_element).select_by_visible_text(str(select_options)); break

                    # interrompe a execução caso o select_type informado seja inválido
                    else: raise Exception('Não foi informado um modo de seleção válido')

                else:
                    execution_error = '[ERRO] Element is not displayed or enabled'
                    optional_attempts = (optional_attempts - 1)

            except Exception as exception_error:
            # registra o erro ocorrido e diminui o contador de tentativas
                time.sleep(1)
                execution_error = exception_error
                optional_attempts = (optional_attempts - 1)

        # gera o relatório de erros e para a execução (caso a intereção não tenha sido realizada)
        if(optional_attempts == 0):
            execution_error = ('[Detalhes do Erro]: {}\n[Elemento]: By.{} "{}"'.format(execution_error, by, element))

            if(optional_by != None and optional_element != None): 
                execution_error = ('{}\n[Elemento Opcional]: By.{} "{}"'.format(execution_error, optional_by, optional_element))

            self.global_tools.generate_report_execution(execution_error, optional_terminate_application=optional_terminate_application)

        else: return True