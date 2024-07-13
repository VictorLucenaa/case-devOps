import os
import yaml


print('Inicializando o script')
# Criar o arquivo logs.txt na mesma raiz do script
with open('logs.txt', 'w') as log_file:
    pass

# Função para remover a propriedade "redis" ou "redisConfig" de um arquivo YAML
def remove_redis_property(yaml_data):
    modified = False
    if 'redis' in yaml_data:
        del yaml_data['redis']
        modified = True
    if 'redisConfig' in yaml_data:
        del yaml_data['redisConfig']
        modified = True
    return modified

# Função para remover a anotação "nginx.ingress.kubernetes.io/ssl-redirect" da propriedade "ingress"
def remove_ingress_ssl_redirect(ingress_data):
    if 'annotations' in ingress_data and 'nginx.ingress.kubernetes.io/ssl-redirect' in ingress_data['annotations']:
        del ingress_data['annotations']['nginx.ingress.kubernetes.io/ssl-redirect']
        return True
    return False

# Função para atualizar a propriedade "version" no arquivo "kustomization.yaml"
def update_kustomization_version(file_path, yaml_data):
    modified = False
    if 'helmCharts' in yaml_data:
        for chart in yaml_data['helmCharts']:
            if chart['version'] != '2.2.1':
                chart['version'] = '2.2.1'
                modified = True
    if modified:
        with open(file_path, 'w') as file:
            yaml.dump(yaml_data, file, default_flow_style=False, sort_keys=False)
        with open('logs.txt', 'a') as log_file:
            log_file.write(f"Modificações realizadas no arquivo: {file_path}\n")
            log_file.write("- Atualizada versão na propriedade 'helmCharts' para '2.2.1'\n")
    return modified

# Função para atualizar o arquivo YAML com as modificações
def update_yaml_file(file_path, yaml_data, modifications):
    with open(file_path, 'w') as file:
        yaml.dump(yaml_data, file, default_flow_style=False, sort_keys=False)
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"Modificações realizadas no arquivo: {file_path}\n")
        for modification in modifications:
            log_file.write(f"- {modification}\n")

# Função para percorrer o diretório atual e suas subpastas
def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        if 'kustomization.yaml' in files:
            kustomization_path = os.path.join(root, 'kustomization.yaml')
            with open(kustomization_path, 'r') as file:
                try:
                    yaml_data = yaml.safe_load(file)
                    if update_kustomization_version(kustomization_path, yaml_data):
                        print(f"Propriedade 'version' atualizada no arquivo: {kustomization_path}")
                        with open('logs.txt', 'a') as log_file:
                            log_file.write(f"Modificações realizadas no arquivo: {kustomization_path}\n")
                            log_file.write("- Atualizado o valor de 'version' para '2.2.1'\n")
                except yaml.YAMLError as e:
                    print(f"Erro ao processar o arquivo {kustomization_path}: {e}")
        for file in files:
            if file.endswith('.yml') or file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    try:
                        yaml_data = yaml.safe_load(file)
                        modifications = []
                        if remove_redis_property(yaml_data):
                            modifications.append("Remover propriedade 'redis' ou 'redisConfig'")
                        if 'ingress' in yaml_data and remove_ingress_ssl_redirect(yaml_data['ingress']):
                            modifications.append("Remover anotação 'nginx.ingress.kubernetes.io/ssl-redirect' da propriedade 'ingress'")
                        if modifications:
                            update_yaml_file(file_path, yaml_data, modifications)
                            print(f"Modificações realizadas no arquivo: {file_path}")
                    except yaml.YAMLError as e:
                        print(f"Erro ao processar o arquivo {file_path}: {e}")

# Chamar a função para processar o diretório atual
process_directory(os.getcwd())