# Plano auditado: Resident Evil 2 DODI

Este plano é aceito apenas para o Setup.exe com SHA-256 `e1184c8459ecf9e20a4dc87ba3dacf8993ccab8a03fa53856b8a2b50976ea36b`. O instalador lê o script Pascal embutido no Setup e chama, nesta ordem, `ISDoneInit(records.inf, 5555, 0, 0, 0, hwnd, 512, callback)`, `ISArcExtract` para cada volume selecionado e `ISDoneStop`.

Volumes principais: `data1.doi` e `data2.doi`. O conteúdo opcional é `Wallpaper.doi`. O helper PE32 em `libexec/isdone-helper.exe` carrega o `ISDone.dll` original extraído do Setup e executa as chamadas ISDone dentro do Wine. O callback PascalScript usa um par função/contexto; o helper preserva essa convenção.

## Proteções e retomada

- A identidade do pacote e dos arquivos selecionados fica no journal do destino.
- Cada volume concluído é verificado pela lista FreeArc de caminhos e tamanhos.
- Uma falha mantém staging, prefixo e logs para permitir diagnóstico ou retomada.
- A pasta final só aparece após todos os volumes selecionados passarem na verificação.
- O destino, prefixo, temporários e logs devem estar em um disco de dados montado; o NVMe do sistema é recusado.

## Resultado no computador

Em 4 de novembro de 2026, o fluxo CLI completo foi executado em `/mnt/Eita/.work/dodi-validation/cli-finished`. O `data1.doi` previamente extraído pelo mesmo helper foi reaproveitado, e o CLI extraiu `data2.doi` e `Wallpaper.doi`. Os três volumes passaram na verificação de nomes e tamanhos. Os 87 arquivos, 26.087.258.415 bytes, também tiveram hashes SHA-256 idênticos aos arquivos correspondentes da instalação existente. Ela contém seis arquivos adicionais sob `Uninstall/`, que o extrator de volumes não cria.

O journal terminou como `complete`. O processo DODI, o helper e os processos Wine foram encerrados. A saída de validação está em `/mnt/Eita/.work/dodi-validation/cli-finished`; o estado e logs estão ao lado, em `.cli-finished.dodi-state`.
