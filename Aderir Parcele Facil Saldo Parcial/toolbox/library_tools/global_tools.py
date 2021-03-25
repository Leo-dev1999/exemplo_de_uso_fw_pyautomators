# =================================================================== #
#                         DESCRIÇÃO DO ARQUIVO                        #
# =================================================================== #
# Descrição: Conjunto de funcionalidades desenvolvidas de uso geral   #
#            por qualquer sistema/programação.                        #
# Empresa: Indra Company (www.indracompany.com)                       #
# Desenvolvedor: Douglas da Silva Garcia / Leonardo R. Evangelista    #
# Atualização: 13 / Novembro / 2019                                   #
# =================================================================== #

# =================================================================== #
#                         COLEÇÃO DE IMPORTS                          #
# =================================================================== #
import os
import re
import shutil
import random
import datetime
import pyautogui
from enum import Enum
from pathlib import Path
from unidecode import unidecode

# =================================================================== #
#                         DEFINIÇÕES DE CLASSE                        #
# =================================================================== #
class convert_to(Enum):
# Classe contendo as opções utilizadas na função convert_month_to
    index = 'index'
    written_name = 'written_name'

class global_tools():

# =================================================================== #
#                         CATÁLOGO DE FUNÇÕES                         #
# =================================================================== #
    def remove_accents(self, word):
    # Função que remove os acentos da string informada
        return unidecode(word)

    def remove_special_characters(self, word):
    # Função que remove os caracteres especiais da string informada
        return re.sub('[!, @, #, $, %, ¨, &, *, ?, /, \, <, >, :, °, ª, º, §, |, ¬, ¢, £, ", ]', '', word)

    def datetime_for_evidences(self):
    # Função que captura a data e hora do sistema e formata o resultado
    # de forma que possa ser utilizado para registro de evidencias.

        # captura a data e hora no momento em que é executada
        date_time = str(datetime.datetime.now()).split('.')
        date_time = date_time[0].split()

        # formata as informações da data
        date = date_time[0].split('-')
        date[1] = self.convert_month_to(convert_to.written_name, date[1])
        date = 'data: {} de {} de {}'.format(date[2], date[1], date[0])

        # formata as informações de horário
        time = date_time[1].split(':')
        time = ('{}h:{}min:{}seg'.format(time[0], time[1], time[2]))

        # retorna as informações de data e hora
        return ('[{} - {}]'.format(date, time))

    def datetime_for_archives(self):
    # Função que captura a data e hora do sistema e formata o resultado
    # de forma que possa ser utilizado no nome dos arquivos

        # captura a data e hora no momento em que é executada
        date_time = str(datetime.datetime.now()).split('.')
        date_time = date_time[0].split()

        # formata as informações da data
        date = date_time[0]

        # formata as informações de horário
        time = date_time[1].split(':')
        time = ('{}h{}min{}seg'.format(time[0], time[1], time[2]))

        # retorna as informações de data e hora
        return ('data[{}_{}]'.format(date, time))

    def convert_month_to(self, convert_to, month):
    # Função que converte índice para nome (e vice-versa) referente ao mês informado

        # cria as listas contendo os índices e nomes de cada mês
        month_by_index = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        month_by_name = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 
                         'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

        # realiza a conversão solicitada
        if(convert_to.name == 'index'):
            try: month = month_by_index[month_by_name.index(month)]
            except: raise Exception ('[ERRO] Não foi informado um mês válido')

        elif(convert_to.name == 'written_name'):
            try: month = month_by_name[month_by_index.index(self.remove_accents(month.lower().strip()))]
            except: raise Exception ('[ERRO] Não foi informado um mês válido')

        else: raise Exception ('[ERRO] Não foi informado um modo de conversão válido')

        # retorna o valor do mês convertido
        return month

    def check_if_file_exists(self, file_path):
    # Função que verifica se existe algum arquivo no caminho informado

        # valida o caminho informado
        if(file_path.strip() == ''):
            raise Exception ('[ERRO] Não foi informado um caminho válido')

        # verifica se o arquivo existe no caminho passado por parâmetro
        if(os.path.isfile(file_path.strip()) == True): return True

        return False

    def check_if_directory_exists(self, directory_path):
    # Função que verifica se existe algum diretório no caminho informado

        # valida o caminho informado
        if(directory_path.strip() == ''):
            raise Exception ('[ERRO] Não foi informado um caminho válido')

        # verifica se o diretório existe no caminho passado por parâmetro
        if(os.path.isdir(directory_path.strip()) == True): return True

        return False

    def delete_file(self, directory_path, file_name):
    # Função responsável por excluir o arquivo informado por parâmetro

        # valida os parâmetros informados
        if(directory_path.strip() == '' or file_name.strip() == ''):
            raise Exception('[ERRO] Os parâmetros informados são inválidos')

        # verifica se o diretório informado possui o arquivo desejado
        if(self.check_file_in_directory(directory_path, file_name) == False):
            raise Exception('[ERRO] O diretório não possui o arquivo informado')

        # realiza a exclusão do arquivo
        try: os.remove('{}/{}'.format(directory_path.lower(), file_name.lower()))
        except: raise Exception ('[ERRO] Houve um erro ao tentar realizar a exclusão do arquivo')

        # valida a exclusão
        if(self.check_file_in_directory(directory_path, file_name) == False): return True

        return False

    def delete_directory(self, directory_path):
    # Função responsável por excluir o diretório informado por parâmetro

        # valida os parâmetros informados
        if(directory_path.strip() == ''):
            raise Exception('[ERRO] Os parâmetros informados são inválidos')

        # verifica se o diretório informado existe
        if(self.check_if_directory_exists(directory_path) == False):
            raise Exception('[ERRO] O diretório informado não existe')

        # realiza a exclusão do diretório
        try: shutil.rmtree(directory_path.strip(), True)

        except: raise Exception ('[ERRO] Houve um erro ao tentar realizar a exclusão do diretório')

        # valida a exclusão
        if(self.check_if_directory_exists(directory_path) == False): return True

        return False

    def create_directory(self, directory_path):
    # Função responsável por criar um diretório no local onde foi informado por parâmetro

        # valida os parâmetros informados
        if(directory_path.strip() == ''):
            raise Exception('[ERRO] Os parâmetros informados são inválidos')

        # verifica se no caminho informado já existe o diretório
        if(self.check_if_directory_exists(directory_path) == True):
            raise Exception('[ERRO] O diretório informado já existe')

        # realiza a criação do diretório
        try: os.mkdir(directory_path.strip())
        except: raise Exception ('[ERRO] Erro ao tentar criar o diretório')

        # valida a criação do diretório
        if(self.check_if_directory_exists(directory_path) == True): return True

        return False

    def check_file_in_directory(self, directory_path, file_name):
    # Função que verifica todos os arquivos dentro de um determinado diretório
    # e retorna de existe algum arquivo que satisfaça as condições informadas nos parâmetros

        # valida os parâmetros informados
        if(directory_path.strip() == '' or file_name.strip() == ''):
            raise Exception('[ERRO] Os parâmetros informados são inválidos')

        # verifica se o diretório informado existe
        if(self.check_if_directory_exists(directory_path) == False):
            raise Exception('[ERRO] O diretório informado não existe')  

        # le todo o conteudo do diretório e verifica se existe algum arquivo
        # que atenda as condições informadas nos parâmetros
        for path, folder, files in os.walk(os.path.abspath(directory_path)):
            for file in files:
                if(str(file).lower() == file_name.strip().lower()):
                    return True

        return False

    def list_directory_files(self, directory_path, optional_file_extension = None):
    # Função que lista todos os arquivos do diretório informado
    # opcionalmente, esta função pode retornar apenas os arquivos com uma determinada extensão

        # definição das variáveis
        file_list = []
        file_extension = ''

        # valida os parâmetros informados
        if(directory_path.strip() == '' or optional_file_extension == ''):
            raise Exception('[ERRO] Os parâmetros informados são inválidos')

        # verifica se o diretório informado existe
        if(self.check_if_directory_exists(directory_path) == False):
            raise Exception('[ERRO] O diretório informado não existe')

        # realiza a leitura de todos os arquivos do diretório
        for path, folder, files in os.walk(os.path.abspath(directory_path)):
            for file in files:
                if(optional_file_extension != None):
                    file_extension = self.check_file_extension(directory_path, file)

                    if(optional_file_extension == file_extension):
                        file_list.append(os.path.join(file))

                else: file_list.append(os.path.join(file))

        # retorna a lista de arquivos obtida
        return file_list

    def check_file_extension(self, directory_path, file_name):
    # Função que verifica a extensão do arquivo passado nos parâmetros

        # definição das variáveis
        directory = Path(directory_path)

        # valida os parâmetros informados
        if(directory_path.strip() == '' or file_name.strip() == ''):
            raise Exception('[ERRO] Os parâmetros informados são inválidos')

        # verifica se o diretório informado existe
        if(self.check_if_directory_exists(directory_path) == False):
            raise Exception('[ERRO] O diretório informado não existe')

        # pega a extensão do arquivo informado
        for file in directory.glob('*'):
            if(file_name == file.name):
                return file.suffix

        return None

    def cpf_generator(self):
    # Função que gera e valida um número de cpf aleatório

        # gera os numeros do cpf
        num_1 = random.randrange(10)
        num_2 = random.randrange(10)
        num_3 = random.randrange(10)
        num_4 = random.randrange(10)
        num_5 = random.randrange(10)
        num_6 = random.randrange(10)
        num_7 = random.randrange(10)
        num_8 = random.randrange(10)
        num_9 = random.randrange(10)

        # gera e valida o primeiro dígito do cpf
        value_1 = num_9 * 2
        value_2 = num_8 * 3
        value_3 = num_7 * 4
        value_4 = num_6 * 5
        value_5 = num_5 * 6
        value_6 = num_4 * 7
        value_7 = num_3 * 8
        value_8 = num_2 * 9
        value_9 = num_1 * 10

        digit_1 = (value_1 + value_2 + value_3 + 
                   value_4 + value_5 + value_6 + 
                   value_7 + value_8 + value_9)
        digit_1 = (11 - round(digit_1 % 11))

        if(digit_1 >= 10): digit_1 = 0

        # gera e valida o segundo dígito do cpf
        value_1 = digit_1 * 2
        value_2 = num_9 * 3
        value_3 = num_8 * 4
        value_4 = num_7 * 5
        value_5 = num_6 * 6
        value_6 = num_5 * 7
        value_7 = num_4 * 8
        value_8 = num_3 * 9
        value_9 = num_2 * 10
        value_10 = num_1 * 11

        digit_2 = (value_1 + value_2 + value_3 + 
                   value_4 + value_5 + value_6 + 
                   value_7 + value_8 + value_9 + value_10)
        digit_2 = (11 - round(digit_2 % 11))

        if(digit_2 >= 10): digit_2 = 0

        # retorna o valor do cpf
        return ("{}{}{}{}{}{}{}{}{}{}{}".format(num_1, num_2, num_3, num_4, num_5, 
                                                num_6, num_7, num_8, num_9, digit_1, digit_2))

    def cnpj_generator(self, generate_with_punctuation = False):
    # Função que gera e valida um número de cnpj aleatório

        # definição das variáveis
        validator = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 6]
        cnpj = [random.randrange(10) for i in range(8)] + [0, 0, 0, 1]

        # gera e valida o primeiro dígito do cnpj
        auxiliary_value = sum(x * y for x, y in zip(reversed(cnpj), validator))
        digit_1 = (11 - auxiliary_value % 11)

        if(digit_1 >= 10): digit_1 = 0
        cnpj.append(digit_1)

        # gera e valida o segundo dígito do cnpj
        auxiliary_value = sum(x * y for x, y in zip(reversed(cnpj), validator))
        digit_2 = (11 - auxiliary_value % 11)

        if(digit_2 >= 10): digit_2 = 0
        cnpj.append(digit_2)

        # retorna o cnpj gerado
        if(generate_with_punctuation == True): return "%d%d.%d%d%d.%d%d%d/%d%d%d%d-%d%d" % tuple(cnpj)
        else: return "%d%d%d%d%d%d%d%d%d%d%d%d%d%d" % tuple(cnpj)

    def generate_report_execution(self, file_text,
                                  optional_file_name = 'report_execution.txt',
                                  optional_image_name = 'report_execution.png',
                                  optional_terminate_application = False):
    # Função responsável por gerar o relatório com base nos parâmetros informados,
    # opcionalmente incluindo um print da tela e podendo parar a execução do script.    

        # valida os parâmetros informados
        if(str(file_text).strip() == '' or optional_file_name == '' or optional_image_name == ''):
            raise Exception('[ERRO] Os parâmetros informados são inválidos')

        # definição das variáveis
        file_path = '{}\\artefact\\documents\\{}'.format(os.getcwd(), optional_file_name)
        image_path = '{}\\artefact\\images\\{}'.format(os.getcwd(), optional_image_name)
        screenshot_module = pyautogui.screenshot()

        # verifica a existência dos diretórios
        if(self.check_if_directory_exists('{}\\artefact\\'.format(os.getcwd())) == False):
            try: self.create_directory('{}\\artefact\\'.format(os.getcwd()))
            except: raise Exception('[ERRO] os diretórios utilizados para salvar os arquivos do relatório não existem')

        if(self.check_if_directory_exists('{}\\artefact\\documents\\'.format(os.getcwd())) == False):
            try: self.create_directory('{}\\artefact\\documents\\'.format(os.getcwd()))
            except: raise Exception('[ERRO] os diretórios utilizados para salvar os arquivos do relatório não existem')

        if(self.check_if_directory_exists('{}\\artefact\\images\\'.format(os.getcwd())) == False):
            try: self.create_directory('{}\\artefact\\images\\'.format(os.getcwd()))
            except: raise Exception('[ERRO] os diretórios utilizados para salvar os arquivos do relatório não existem')

        # tenta remover os acentos da string
        try: file_text = self.remove_accents(file_text)
        except: pass

        # grava as informações solicitadas
        try:
            archive = open(file_path, 'a')
            archive.writelines('"{}"'.format(file_text))
            archive.writelines('\n"{}"'.format(self.datetime_for_evidences()))
            archive.writelines('\n')
            screenshot_module.save(r'{}'.format(image_path))

        except Exception as exception_error: raise Exception(exception_error)

        finally: archive.close()

        # interrompe a execução do script
        if(optional_terminate_application == True):
            raise Exception('Execução encerrada, verifique o relatório gerado para maiores informações')

        # verifica se os arquivos do relatório foram gerados
        if(self.check_if_file_exists(file_path) == True and 
        self.check_if_file_exists(image_path) == True): return True

        return False