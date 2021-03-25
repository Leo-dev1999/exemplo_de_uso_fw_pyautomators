# =================================================================== #
#                         DESCRIÇÃO DO ARQUIVO                        #
# =================================================================== #
# Descrição: Este arquivo contem a classe responsavel por construir   #
#            a toolbox que será utilizada pela aplicação              #
# Empresa: Indra Company (www.indracompany.com)                       #
# Desenvolvedor: Douglas da Silva Garcia / Leonardo R. Evangelista    #
# Atualização: 25 / Novembro / 2019                                   #
# =================================================================== #

# =================================================================== #
#                         COLEÇÃO DE IMPORTS                          #
# =================================================================== #
from toolbox.library_tools.global_tools import global_tools
from toolbox.library_tools.selenium_tools import selenium_tools
from toolbox.project_tools.csf_general_tools import csf_tools
from selenium.webdriver.common.action_chains import ActionChains

# =================================================================== #
#                         DEFINIÇÕES DE CLASSE                        #
# =================================================================== #
class toolbox(csf_tools, global_tools, selenium_tools):
    def __init__(self, service, functionality, scenario):

        # carrega as informações baseadas no cenario do teste
        self.selected_dictionary = self.load_inventory(service, functionality, scenario)
        self.global_tools = global_tools()

        # caso o valor da flag executar_automacao seja True
        # o driver do selenium é iniciado
        if(self.selected_dictionary['features']['executar_automacao'] == True):
            self.selenium_webdriver = selenium_tools(self.selected_dictionary['features']['navegador']).import_webdriver()
            self.action_chains = ActionChains(self.selenium_webdriver)