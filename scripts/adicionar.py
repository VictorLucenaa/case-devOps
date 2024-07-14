import os
import yaml
from datetime import datetime
import logging
import argparse

# Adiciona a opção de linha de comando para dry-run
parser = argparse.ArgumentParser(description='Script de adição')
parser.add_argument('--dry-run', action='store_true', help='Executar em modo dry-run (não aplicar modificações)')
args = parser.parse_args()

print('Script de adição inicializado. Verifique os resultados no arquivo "logs_de_adicao.txt"')
# Cria o arquivo de monitoramento dos logs logs_de_adicao.txt na raiz
with open('logs_de_adicao.txt', 'w') as log_file:
    pass

# Configuração de logs para erros
logging.basicConfig(
    filename='logs_de_adicao.txt',
    level=logging.INFO,
    format='[%(asctime)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Função que atualiza a propriedade "version" no arquivo "kustomization.yaml"
def update_kustomization_version(file_path, yaml_data):
    modified = False
    if 'helmCharts' in yaml_data:
        for chart in yaml_data['helmCharts']:
            if chart['version'] != '2.2.1':
                chart['version'] = '2.2.1'
                modified = True
    if modified:
        with open(file_path, 'w') as file:
            yaml.dump(yaml_data, file, default_flow_style=False, sort_keys=True)
        with open('logs_de_adicao.txt', 'a') as log_file:
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            log_file.write(f"\n[{timestamp}] - Modificações realizadas no arquivo: {file_path}\n")
            log_file.write("- Atualizado o valor de 'version' na configuração 'helmCharts' para '2.2.1'\n")
    return modified

# Função que atualiza as propriedades da configuração "ports"
def update_ports_configuration(yaml_data):
    modified = False
    if 'ports' in yaml_data:
        yaml_data['ports'] = [
            {
                "name": "http",
                "containerPort": "$PORT",
                "protocol": "TCP"
            }
        ]
        modified = True
    return modified

# Função para atualizar o arquivo YAML com as modificações
def update_yaml_file(file_path, yaml_data, modifications):
    modified = False
    if 'env' in yaml_data and yaml_data['env'] != 'ENV:dev':
        yaml_data['env'] = 'ENV:dev'
        modified = True
        with open('logs_de_adicao.txt', 'a') as log_file:
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            log_file.write(f"\n[{timestamp}] - Modificações realizadas no arquivo: {file_path}\n")
            log_file.write("- Atualizado valor da propriedade 'env' para 'ENV:dev'\n")
    if modified or modifications:
        if not args.dry_run:
            with open(file_path, 'w') as file:
                yaml.dump(yaml_data, file, default_flow_style=False, sort_keys=True)
        if modifications:
            with open('logs_de_adicao.txt', 'a') as log_file:
                for modification in modifications:
                    log_file.write(f"- {modification}\n")
    return modified or bool(modifications)

# Função para atualizar os valores da propriedade "limits" 
def update_cpu_limits(yaml_data):
    modified = False
    for key, value in yaml_data.items():
        if isinstance(value, dict) and 'limits' in value:
            if 'cpu' in value['limits']:
                if value['limits']['cpu'] != '100m':
                    value['limits']['cpu'] = '100m'
                    modified = True
    return modified

# Função para atualizar os valores da propriedade "requests" 
def update_cpu_requests(yaml_data):
    modified = False
    for key, value in yaml_data.items():
        if isinstance(value, dict) and 'requests' in value:
            if 'cpu' in value['requests']:
                if value['requests']['cpu'] != '10m':
                    value['requests']['cpu'] = '10m'
                    modified = True
    return modified

# Função para percorrer o diretório atual e suas subpastas
def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        if 'kustomization.yaml' in files:
            kustomization_path = os.path.join(root, 'kustomization.yaml')
            with open(kustomization_path, 'r') as file:
                try:
                    yaml_data = yaml.safe_load(file)
                    if update_kustomization_version(kustomization_path, yaml_data):
                        pass
                except yaml.YAMLError as e:
                    logging.error(f"Erro ao processar o arquivo {kustomization_path}: {e}")
        for file in files:
            if file.endswith('.yml') or file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    try:
                        yaml_data = yaml.safe_load(file)
                        modifications = []
                        if update_ports_configuration(yaml_data):
                            modifications.append(f"Atualizadas as propriedades de 'ports' para name: http, containerPort: $PORT, protocol: TCP")
                        if update_cpu_requests(yaml_data):
                            modifications.append("Atualizadas as configurações 'requests' para 10m")
                        if update_cpu_limits(yaml_data):
                            modifications.append("Atualizadas as configurações de 'limits' para 100m")    
                        if update_yaml_file(file_path, yaml_data, modifications):
                            pass
                    except yaml.YAMLError as e:
                        logging.error(f"Erro ao processar o arquivo {file_path}: {e}")

# Chamar a função para processar o diretório atual
process_directory(os.getcwd())