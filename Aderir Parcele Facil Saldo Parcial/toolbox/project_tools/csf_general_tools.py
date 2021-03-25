# =================================================================== #
#                         DESCRIÇÃO DO ARQUIVO                        #
# =================================================================== #
# Descrição: Conjunto de funcionalidades desenvolvidas para           #
#            o projeto de testes regressivos do banco CSF             #
# Empresa: Indra Company (www.indracompany.com)                       #
# Desenvolvedor: Douglas da Silva Garcia / Leonardo R. Evangelista    #
# Atualização: 25 / Novembro / 2019                                   #
# =================================================================== #

# =================================================================== #
#                         COLEÇÃO DE IMPORTS                          #
# =================================================================== #
import os
import yaml

# =================================================================== #
#                         DEFINIÇÕES DE CLASSE                        #
# =================================================================== #
class csf_tools():

# =================================================================== #
#                         CATÁLOGO DE FUNÇÕES                         #
# =================================================================== #
    def load_inventory(self, service, functionality, scenario):
    # Função responsavel por carregar os arquivos de inventory
    # criando um dicionario contendo as informações coletadas destes arquivos

        # definição das variáveis
        inventory = {}

        try:
            # carrega as informações do inventory
            data_inventory = yaml.load(open('./manager/data_inventory.yml', 'r'), Loader=yaml.Loader)
            object_inventory = yaml.load(open('./manager/object_inventory.yml', 'r'), Loader=yaml.Loader)
            features_inventory = yaml.load(open('./manager/features_inventory.yml', 'r'), Loader=yaml.Loader)

            # carrega as informações do inventory com base nos parâmetros informados
            inventory['data'] = data_inventory[service][functionality][scenario]
            inventory['object'] = object_inventory[service][functionality][scenario]
            inventory['features'] = features_inventory[service][functionality][scenario]

            # retorna o dicionario preenchido
            return inventory

        # caso ocorra algum erro a aplicação é encerrada
        except Exception as exception_error:
            raise Exception('[ERRO] Não foi possivel realizar a criação do dicionario inventory.\nDetalhes do erro: {}'.format(exception_error))

    def generate_report_automation(self, functionality, feature_inventory, execution_result):
    # Função responsavel por gerar o relatório referente a execução realizada
    # informando quais funcionalidades e cenarios foram executados/testados

        # definição das variáveis
        block_separator = '# =================================================================== #'
        datetime_report = self.datetime_for_evidences()

        # verifica se o diretório existe
        if(self.check_if_directory_exists('{}\\artefact\\documents\\'.format(os.getcwd())) == False):
            raise Exception('[ERRO] os diretórios utilizados para salvar os arquivos do relatório não existem')

        try:
            archive = open('./artefact/documents/report_automation.txt', 'a')

            # grava as informações no relatório
            archive.writelines('{}\n'.format(block_separator))
            archive.writelines('Funcionalidade: {}\n'.format(functionality))
            archive.writelines('Descricao: {}\n'.format(feature_inventory['descricao']))
            archive.writelines('Tag: {}\n'.format(feature_inventory['tag']))
            archive.writelines('Navegador: {}\n'.format(feature_inventory['navegador']))
            archive.writelines('Url: {}\n'.format(feature_inventory['url']))
            archive.writelines('Resultado: {}\n'.format(execution_result))
            archive.writelines(datetime_report)
            archive.writelines('\n')

        # caso ocorra algum erro a aplicação é encerrada
        except Exception as exception_error:
            raise Exception('[ERRO] Não foi possivel gravar as informações no relatório.\nDetalhes do erro: {}'.format(exception_error))

        # fecha o arquivo
        finally: archive.close()