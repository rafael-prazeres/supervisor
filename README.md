##### Descrição do funcionamento do script:

* Recebe entradas via arquivo de texto
* Cria tabela de pastas e ajusta permissões usando a api Google Drive
* Cria eventos e salas de videochamada indicados no documento Comissão e Calendário de Provas usando a api Google Calendar

##### Fontes:

* https://developers.google.com/drive/api/v3/quickstart/python
* https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/
* https://developers.google.com/calendar/v3/reference/events/insert

##### Instruções de uso:

* Instalar python
	* No windows
		* https://www.youtube.com/watch?v=gDxt7mncWys
* Instalar a Biblioteca Cliente do Google
	* Executar no prompt de comandos (windows) ou no bash (linux)
		* pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
* Criar arquivo de entrada seguindo modelo proposto no arquivo exemplo_entrada.txt localizado na pasta raiz do projeto
	* No caso do windows salvar com Encoding ANSI
* Solicitar token de acesso à agenda do Google no grupo dos supervisores de gravação de prova didática no whatsapp
	* Salvar o token na mesma pasta do script
	* Como faço para gerar meu próprio token?
		* Enable the Drive API
			* https://developers.google.com/drive/api/v3/quickstart/python 
* Executar o script
	* No windows, pelo prompt de comandos
		* python supervisor.py < entrada.txt
	* No linux:
		* cat entrada.txt | python3 supervisor.py

