# Easy-DODI-Installer-for-Linux
A standalone Linux CLI for extracting DODI repacks, with an interactive menu for content and destination selection.

# Executável standalone

O arquivo pronto é `dist/dodi` (aproximadamente 92 MB). Copie-o para a pasta do repack e execute `./dodi`. Também aceita `./dodi /caminho/Setup.exe`. Sem argumentos, usa somente a pasta atual ou a pasta do próprio executável, sem varrer discos.

O menu pergunta conteúdo opcional, disco/pasta e confirmação. Não fornece respostas automaticamente. O runtime incluído (Wine e helpers) é preparado em `/mnt/SSD/Tools/dodi-cli`, marcado com `NAO_APAGAR.txt`. Exige Linux x86-64, Python 3 e bibliotecas básicas do sistema; não é um binário independente de qualquer distribuição. O Setup original fornece os codecs, mas sua interface gráfica não é executada no fluxo padrão.

A extração direta está validada para o pacote Resident Evil 2 auditado; outros pacotes ainda precisam de suporte específico. Empacotamento e menu foram verificados sem iniciar outra extração completa.

Recompilar: `python3 tools/build-standalone.py`.

# DODI Installer for Linux

Instalador de terminal para pacotes DODI locais. Informe o caminho do `Setup.exe`, de um volume `.doi` ou da pasta do pacote; o programa então confere os volumes e apresenta as opções de destino e conteúdo. Sem argumento, ele pede o caminho. Não procura pacotes automaticamente.

O projeto está em `/mnt/SSD/github/rune`. Por padrão, saída, temporários, logs e prefixo Wine ficam no disco de dados `/mnt/Eita`; `/mnt/SSD` também pode ser escolhido. O NVMe do sistema é bloqueado para esses arquivos.

## Uso

```sh
./dodi                         # pede o caminho do pacote
./dodi "/caminho/Setup.exe"     # abre as opções desse pacote
./dodi --scan                  # procurar pacotes (somente quando solicitado)
./dodi --plan                  # mostrar o plano sem extrair
./dodi --gui                   # abrir o Setup original
./dodi "/caminho/da/pasta"      # abre as opções desse pacote
```

O modo padrão de terminal usa os próprios componentes ISDone do pacote. No menu, escolha o destino e os opcionais; a extração ocorre por volume, com retomada registrada em journal. Após cada volume, o programa confere os caminhos e tamanhos dos arquivos com a listagem do arquivo de origem. O jogo é publicado no destino só depois da validação.

`--gui` abre o `Setup.exe` original pelo Wine corrigido já disponível em `/mnt/Eita/Tools/fitgirl-wine`. O modo de terminal não executa as etapas adicionais de instalação do Setup, como criar um desinstalador ou oferecer pré-requisitos; ele extrai os volumes selecionados.

## Compatibilidade validada

O plano direto está deliberadamente limitado ao `Setup.exe` auditado do Resident Evil 2 deste computador (SHA-256 `e1184c8459ecf9e20a4dc87ba3dacf8993ccab8a03fa53856b8a2b50976ea36b`). A sequência recuperada do script do instalador é `ISDoneInit` → `ISArcExtract` → `ISDoneStop`. Outros pacotes precisam ser auditados antes de usar esse caminho; use `--gui` neles.

O teste integrado local extraiu `data1.doi`, `data2.doi` e `Wallpaper.doi` no Eita e validou todos os arquivos pelo nome e tamanho. O resultado incluiu 87 arquivos dos três volumes; os seis arquivos adicionais da instalação original pertencem ao desinstalador criado pelo Setup. Veja [docs/PLAN_RE2.md](docs/PLAN_RE2.md) e [docs/REFERENCES.md](docs/REFERENCES.md).

## Requisitos

- Linux x86-64, Python 3 e a build Wine indicada acima.
- Pacote local com `Setup.exe` e volumes `.doi` correspondentes.
- Disco de dados montado com espaço para a extração e arquivos temporários.

O instalador trabalha com os arquivos locais encontrados e não baixa conteúdo.
