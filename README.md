# jogoslakers

Consulta de calendário, placares e resultados do Los Angeles Lakers usando o
endpoint público da ESPN. Requer Python 3.10+ e não precisa de pacotes ou chave.
Essa API não oficial pode mudar ou ficar indisponível, sem garantia de estabilidade.

```sh
cd /workspace/jogoslakers
python3 lakers.py
python3 lakers.py --season 2026
python3 lakers.py --season 2026 --seasontype 3
```

O comando retorna JSON com data em UTC, status, time da casa, visitante e pontos.
Placares ausentes ficam como `null`. O ano é o de encerramento da temporada;
`2026` representa 2025–26. Sem ano explícito, a fonte escolhe a temporada atual.
Use `--seasontype 1` para pré-temporada, `2` para temporada regular ou `3` para playoffs.

O ambiente precisa permitir HTTPS para `site.api.espn.com`. Em caso de erro de
rede ou resposta incompatível, o comando informa o erro e termina com código 1.
