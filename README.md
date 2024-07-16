<h1 align="center" style="font-weight: bold;">Case técnico DevOps Junior 💻</h1>

<p align="center">
    <b>Este projeto contém dois scripts Python que modificam arquivos YAML. O primeiro script, adicionar.py, atualiza propriedades específicas em arquivos YAML, enquanto o segundo script, remover.py, remove propriedades específicas de arquivos YAML.</b>
</p>

<h2>Scripts</h2>

<h3>adicionar.py</h3>

<p>Este script percorre um diretório e suas subpastas, procurando por arquivos YAML e realiza as seguintes modificações nos arquivos encontrados:
  
- Atualiza o valor da propriedade "version" para "2.2.1" em arquivos "kustomization.yaml".
- Atualiza as subpropriedades da propriedade "ports" para "name: http, containerPort: $PORT, protocol: TCP".
- Atualiza os valores das propriedades "requests" para "10m" e "limits" para "100m".
- Atualiza o valor da propriedade "env" para "ENV:dev".
- Atualiza a ordem das propriedades dos arquivos para que fiquem iguais
  
Este script fornece um modo de simulação (dry-run) que permite verificar as modificações antes de aplicá-las tornando as alterações mais seguras.</p>

<h3>remover.py</h3>

<p> Este script percorre um diretório e suas subpastas, procurando por arquivos YAML e remove propriedades específicas de arquivos YAML, incluindo:
  
- As propriedades "redis" e "redisConfig".
- A anotação "nginx.ingress.kubernetes.io/ssl-redirect" da propriedade "ingress".
- Subpropriedades extras de propriedades com "enabled" = false.
- Propriedades duplicadas
- linhas comentadas
- Atualiza a ordem dos arquivos para que fiquem iguais
  
Este script também fornece o modo de simulação (dry-run) que permite verificar as modificações antes de aplicá-las tornando as alterações mais seguras.
</p>

<h2>💻 Technologias Utilizadas</h2>

- Python

<h2>🚀 Iniciando a aplicação</h2>

<h3>Pré-requisitos</h3>

<p>Antes de iniciar o script, será preciso baixar e instalar os seguintes programas na sua máquina, caso ainda não possua:</p>

- [Python](https://www.python.org/downloads/)
- [Git 2](https://git-scm.com/downloads)

<h3>Clonando</h3>

<p>No terminal ou prompt de comando, navegue até o diretório onde você deseja clonar o repositório e execute este comando:</p>

```bash
git clone https://github.com/VictorLucenaa/case-devOps.git
```

<h3>Instalando as bibliotecas</h3>

<p>No terminal ou prompt de comando, escreva o seguinte comando para instalar as bibliotecas necessárias para utilizar a aplicação:</p>

```bash
pip install pyyaml
```

<h3>Inicializando o script</h3>

<p>Pelo terminal, abra o diretório do arquivo que você baixou</p>

```bash
cd endereço_do_seu_repositório
```

<p>A raiz da sua pasta deve estar assim:</p>

```
case-devOps
├── desafio 1 - pratico
│   ├── adicionar.py
│   ├── remover.py
│   └── Teste - DevOps PSE
│       └── applications
│           ├── admin-auth-back
│           ├── admin-front
│           ├── notification-order-service
│           ├── orders-home-api
│           ├── payments-status-api
│           ├── reports
│           ├── root
│           ├── waiter-front
│           ├── worker-timeout-order
│           ├── worker-upload-img
│           └── worker-validate-order-created
├── desafio 2 - teorico
│   └── desafio teorico.docx
└── README.md
```

<p>Navegue até a pasta desafio 1 - pratico:</p>

```bash
cd case-devOps/desafio 1 - pratico
```

<h2> Executando adicionar.py </h2>

<p>Para executar o script adicionar.py em modo de simulação (dry-run), use o seguinte comando:</p>

```bash
 python adicionar.py --dry-run
```

<p>Isso irá executar o script sem aplicar as modificações, mas gerará um arquivo de log chamado logs_de_adicao.txt com as modificações que seriam feitas.</p>

<p>Para aplicar as modificações, execute o script sem a opção --dry-run:</p>

```bash
python adicionar.py
```

<p>Isso irá aplicar as modificações aos arquivos YAML encontrados no diretório atual e suas subpastas.</p>

<h2> Executando remover.py </h2>

<p>Para executar o script remover.py em modo de simulação (dry-run), use o seguinte comando:</p>

```bash
 python remover.py --dry-run
```

<p>Isso irá executar o script sem aplicar as modificações, mas gerará um arquivo de log chamado logs_de_remocao.txt com as modificações que seriam feitas.</p>

<p>Para aplicar as modificações, execute o script sem a opção --dry-run:</p>

```bash
python remover.py
```

<p>Isso irá aplicar as modificações aos arquivos YAML encontrados no diretório atual e suas subpastas.</p>
