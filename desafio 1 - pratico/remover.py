import os
import yaml
from datetime import datetime
import logging
import argparse

# Adiciona a opção de linha de comando para dry-run
parser = argparse.ArgumentParser(description='Script de remoção')
parser.add_argument('--dry-run', action='store_true', help='Executar em modo dry-run (não aplicar modificações)')
args = parser.parse_args()

print('Script de remoção inicializado, acompanhe as modificações no arquivo "logs_de_remocao.txt"')

# Cria o arquivo de logs logs_de_remocao.txt na mesma raiz do script
with open('logs_de_remocao.txt', 'w') as log_file:
    pass

# Configuração de logs para erros
logging.basicConfig(
    filename='logs_de_remocao.txt',
    level=logging.INFO,
    format='%(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

# Função para remover a propriedade "redis"
def remove_redis_property(yaml_data):
    modified = False
    if 'redis' in yaml_data:
        del yaml_data['redis']
        modified = True
    return modified

# Função para remover a propriedade "redisConfig"
def remove_redisconfig_property(yaml_data):
    modified = False
    if 'redisConfig' in yaml_data:
        del yaml_data['redisConfig']
        modified = True
    return modified

# Função que remove a anotação "nginx.ingress.kubernetes.io/ssl-redirect" da propriedade "ingress"
def remove_ingress_ssl_redirect(ingress_data):
    if 'annotations' in ingress_data and 'nginx.ingress.kubernetes.io/ssl-redirect' in ingress_data['annotations']:
        del ingress_data['annotations']['nginx.ingress.kubernetes.io/ssl-redirect']
        return True
    return False

# Função que remove as propriedades extras das configurações com "enabled" = false
def remove_disabled_configurations(yaml_data):
    modified = False
    removed_keys = []
    for key, value in yaml_data.items():
        if isinstance(value, dict) and 'enabled' in value and not value['enabled']:
            for sub_key in list(value.keys()):
                if sub_key != 'enabled':
                    del value[sub_key]
                    modified = True
                    removed_keys.append(sub_key)
    return modified, removed_keys

# Função para percorrer o diretório atual e suas subpastas
def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.yml') or file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    try:
                        yaml_data = yaml.safe_load(file)
                        modifications = []
                        if remove_redisconfig_property(yaml_data):
                            modifications.append("Removida a propriedade 'redisConfig'")
                        if remove_redis_property(yaml_data):
                            modifications.append("Removida a propriedade 'redis'")
                        if 'ingress' in yaml_data and remove_ingress_ssl_redirect(yaml_data['ingress']):
                            modifications.append("Removida a anotação 'nginx.ingress.kubernetes.io/ssl-redirect' da propriedade 'ingress'")
                        modified, removed_keys = remove_disabled_configurations(yaml_data)
                        if modified:
                            modifications.append(f"Removidas as propriedades extras de configurações com enabled = false: {', '.join(removed_keys)}")
                        if modifications:
                            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                            logging.info(f"\n[{timestamp}] Modificações no arquivo -> %s", file_path)
                            for modification in modifications:
                                logging.info(" - %s", modification)
                            if not args.dry_run:
                                with open(file_path, 'w') as file:
                                    yaml.dump(yaml_data, file, default_flow_style=False, sort_keys=True)
                    except yaml.YAMLError as e:
                        logging.error(f"Erro ao processar o arquivo {file_path}: {e}")

# Chamar a função para processar o diretório atual
process_directory(os.getcwd())