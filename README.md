Smither
======

Smither é uma ferramenta de cálculo para graduados em economia organizada por módulos.

Requisitos
---------
- Python 3.10+ (recomendado)
- Virtualenv (opcional, recomendado)

Instalação das dependências
---------------------------
Na raiz do projeto, crie e use um virtualenv (opcional):

Windows PowerShell (sem ativar o script de ativação):
```powershell
python -m venv .venv
# Para usar o Python do venv sem ativar o script de ativação:
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
```

Windows PowerShell (se quiser ativar o venv e permitir execução de scripts):
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
& ".\.venv\Scripts\Activate.ps1"
pip install -r requirements.txt
```

Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Executando o Smither
--------------------
Você pode rodar o entrypoint principal (recomendado) a partir da raiz do projeto:

```powershell
# Usando o python do venv sem ativar
& ".\.venv\Scripts\python.exe" ".\#Smither.py"
```

Ou executar o módulo do cálculo diretamente (como pacote):

```powershell
& ".\.venv\Scripts\python.exe" -m calculo.menu_calculo
```

Notas importantes
-----------------
- Não execute `calculo/derivadas.py` diretamente com `python calculo/derivadas.py`, pois o módulo usa imports relativos (`from . import engine`) que requerem execução como pacote (via `-m` ou pelo entrypoint).
- Se seu PowerShell bloquear a ativação do venv, use o comando `Set-ExecutionPolicy` mostrado acima (altera apenas o escopo `CurrentUser`).

Suporte e desenvolvimento
-------------------------
- Para adicionar novos módulos crie uma pasta com um arquivo `menu_*.py` que exponha uma função `menu()`.
- Para contribuir, rode os testes locais que você adicionar e abra PRs.

Uso em ambientes sem display (headless)
-------------------------------------

- Por padrão, o Smither tentará abrir janelas de plot (chamando `plt.show()`), o que requer um ambiente gráfico. Em servidores/CI/WSL sem display, os gráficos não podem ser abertos — para esses casos o pacote agora salva automaticamente imagens na pasta `outputs/` em vez de mostrar janelas.
- Para forçar o modo headless (salvar automaticamente) exporte a variável de ambiente `HEADLESS=1` (Linux/macOS) ou defina-a no PowerShell antes de executar:

```powershell
# PowerShell (força salvar ao invés de exibir)
$env:HEADLESS = '1'
& ".\.venv\Scripts\python.exe" ".\#Smither.py"
```

- Alternativamente, nos prompts interativos de plot o programa perguntará como deseja exibir cada gráfico: `(v)er` / `(s)alvar` / `(a)uto` — onde `auto` usa detecção automática (salva se não houver backend gráfico).
- As imagens salvas são colocadas em `outputs/` na raiz do projeto e os nomes de arquivo incluem timestamp. Exemplo: `outputs/gradiente_no_ponto_20260303_162428.png`.

Compatibilidade de terminal
--------------------------
- Se você rodar em Windows PowerShell antigo e vir erros de exibição por causa de caracteres Unicode, execute no PowerShell moderno (Windows Terminal) ou altere sua codificação. Também é possível ajustar os cabeçalhos no código (`calculo/derivadas.py`) para usar textos ASCII simples.
