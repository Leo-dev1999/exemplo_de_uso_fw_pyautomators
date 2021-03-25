# =================================================================== #
#                         COLEÇÃO DE IMPORTS                          #
# =================================================================== #
import os
from toolbox.build_toolbox import toolbox
from automation.servico.pgs_parcele_facil import parcele_facil

# =================================================================== #
#                         CATÁLOGO DE STEPS                           #
# =================================================================== #

# @tag_cen02_parcele_facil
# Cenario: Aderir Parcele Fácil com Saldo Parcial
@given(u'que o usuario esteja logado no FUN e deseja aderir parcele com saldo parcial')
def step_request_02(context):

    # variavel que ira armazenar os erros de execuçção do teste
    context.exception_error = ''

    try:
        # constrói a toolbox com base nos parâmetros informados
        context.toolbox = toolbox('Servico', 'Parcele Facil', 'cenario_02')

        # acessa a página do front-unico e realiza o login
        if(context.toolbox.selected_dictionary['features']['executar_automacao'] == True):
            context.parcele_facil = parcele_facil(context.toolbox)
            context.request_02 = context.parcele_facil.request_02()

        else: context.request_02 = False

    except Exception as exception_error:
        context.request_02 = False
        context.exception_error = exception_error

@when(u'o usuario navega ate a funcionalidade aderir parce facil com saldo parcial')
def step_comparison_02(context):

    try:
        # identifica o cliente e acessa a funcionalidade
        if(context.request_02 == True and context.toolbox.selected_dictionary['features']['executar_automacao'] == True):
            context.comparison_02 = context.parcele_facil.comparison_02()

        else: context.comparison_02 = False

    except Exception as exception_error:
        context.comparison_02 = False
        context.exception_error = exception_error

@then(u'a funcionalidade aderir parcele facil com saldo parcial é acessada')
def step_validation_02(context):

    try:
        # realiza o fluxo da funcionalidade e encerra o atendimento
        if(context.comparison_02 == True and context.toolbox.selected_dictionary['features']['executar_automacao'] == True):
            context.validation_02 = context.parcele_facil.validation_02()
            context.toolbox.selenium_webdriver.close()

        elif(context.toolbox.selected_dictionary['features']['executar_automacao'] == False):
            context.validation_02 = 'Nao Executado'

        else: context.validation_02 = 'Falha'

    except Exception as exception_error:
        context.validation_02 = 'Falha'
        context.exception_error = exception_error

    # encerra o browser e gera o relatório
    context.toolbox.generate_report_automation('Adesão Parcele Facil com Saldo Parcial', context.toolbox.selected_dictionary['features'], context.validation_02)

    # apaga os arquivos de log gerados pela automação
    try: context.toolbox.delete_file(os.getcwd(), 'debug.log')
    except: pass

    # mostra os erros ocorridos durante a execução
    if(context.exception_error != ''): raise Exception(context.exception_error)