# Easy-DODI-Installer-for-Linux

Um CLI standalone para extrair repacks DODI locais no Linux. O menu interativo permite escolher conteúdo opcional e o destino da instalação.

## Início rápido

Copie [`dist/dodi`](dist/dodi) para a pasta do repack e execute:

```sh
./dodi
```

O menu pergunta o idioma e depois apresenta as opções do pacote. Também é possível informar o pacote diretamente:

```sh
./dodi /caminho/para/Setup.exe
```

O standalone inclui as ferramentas de extração e o runtime do Wine. Na primeira execução, prepara o runtime em `/mnt/SSD/Tools/dodi-cli`; mantenha essa pasta. Requer Linux x86-64, Python 3 e bibliotecas comuns do sistema. O runtime está incluído, mas o programa não é um binário estático.

O CLI padrão extrai os volumes selecionados sem executar a interface gráfica original do Setup. Depois de cada volume, confere caminhos e tamanhos dos arquivos, registra o progresso para permitir retomada e só publica a pasta final depois da validação. `--gui` abre o Setup original; `--scan` procura pacotes somente quando solicitado.

## Compatibilidade

A extração direta foi auditada para o pacote Resident Evil 2 usado no desenvolvimento. Outros repacks podem exigir um plano próprio; use `--gui` nesses casos. O teste local do Resident Evil 2 conferiu os três volumes por caminho e tamanho e comparou os hashes SHA-256 dos 87 arquivos extraídos com os da instalação existente. Consulte [o plano de teste](docs/PLAN_RE2.md), a [validação de compatibilidade](docs/COMPATIBILITY.md) e as [referências técnicas](docs/REFERENCES.md).

## Compilação

Execute `python3 tools/build-standalone.py` para gerar `dist/dodi`. Atualmente, o processo espera encontrar o arquivo Wine em `/mnt/Eita/Tools/fitgirl-wine/wine-11.14-fitgirl-amd64.tar.xz`.

A licença não comercial do projeto cobre apenas o código original. Os componentes de terceiros mantêm seus próprios termos; consulte [LICENSE](LICENSE) e [avisos de terceiros](THIRD_PARTY_NOTICES.md).
