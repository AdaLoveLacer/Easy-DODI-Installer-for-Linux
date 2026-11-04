# Referências técnicas

- [Fr4nzz/linux-repack-gaming — guia para instalar repacks com Wine](https://github.com/Fr4nzz/linux-repack-gaming/blob/main/guides/install-repacks-with-wine.md): documenta uma instalação DODI específica com Wine 11.13 corrigido e um wrapper para localizar helpers Oodle 7. O guia também recomenda validar crescimento do destino e não baixar DLLs aleatórias. A versão Oodle 7 do exemplo não corresponde ao `oo2core_5_win64.dll` encontrado no pacote local.
- [Fr4nzz/linux-repack-gaming — repositório](https://github.com/Fr4nzz/linux-repack-gaming): origem da rotina de compatibilidade citada no guia.
- [WineHQ bug 59472](https://list.winehq.org/hyperkitty/list/wine-bugs%40list.winehq.org/thread/24ZXNXCQSI547WH3ZPKGETLBDDGQUBFI/): relato de FreeArc parado no Wine em modo WoW64. É evidência de que o tipo de travamento pode ser compatibilidade de execução; não confirma a causa deste pacote.

As referências acima serviram apenas como contexto sobre Wine e repacks; o suporte específico ao Resident Evil 2 foi recuperado do Setup local. O fluxo direto foi validado em `/mnt/Eita/.work/dodi-validation/cli-finished`, com conferência dos três volumes por caminhos e tamanhos. Os 87 arquivos, totalizando 26.087.258.415 bytes, também tiveram SHA-256 idêntico aos arquivos correspondentes da instalação existente.
