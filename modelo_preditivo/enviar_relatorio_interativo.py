import webbrowser
import urllib.parse
from datetime import datetime

# Entrar com o e-mail
destinatario = input("Digite o e-mail do destinatário: ").strip()
email = outlook.CreateItem(0)

if destinatario:
    assunto = f" Relatório de Matrícula - {datetime.now().strftime('%d/%m/%Y')}"
    corpo = "Olá,\n\nSegue em anexo o relatório de matrícula gerado automaticamente.\n\nAtenciosamente,\nEquipe Shaolin"
    
    mailto_link = f"mailto:{destinatario}?subject={urllib.parse.quote(assunto)}&body={urllib.parse.quote(corpo)}"
    
    print("Abrindo o cliente de e-mail padrão...")
    webbrowser.open(mailto_link)
else:
    print(" Nenhum e-mail informado.")
