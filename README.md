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
* Criar arquivo de entrada seguindo modelo abaixo
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


##### Modelo de Entrada:
numeroEdital/Ano  
ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS  
4  
3  
examinador1@ufrn.edu.br  
examinador2@gmail.com  
examinador3@hotmail.com  
  
supervisor1@ufrn.edu.br  
supervisor2@ufrn.edu.br  
supervisor3@ufrn.edu.br  
  
concursos1@ufrn.edu.br  
concursos2@ufrn.edu.br  
concursos3@ufrn.edu.br  
  
candidato@gmail.com  
candidato@hotmail  
candidato@yahoo.com.br  
candidato@live.com  
  
03/10/2020 14:50  
03/10/2020 15:30  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Sorteio da ordem de apresentação da Didática e Temas do 1º Turno (03 candidatos)  
Sorteio da ordem de apresentação da Didática - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 08:00  
03/10/2020 08:40  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Sorteio dos Temas da Didática - 2º Turno (03 candidatos)  
Sorteio dos Temas da Didática - 2º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 14:00  
03/10/2020 14:40  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Sorteio dos Temas da Didática - 3º Turno (03 candidatos) 
Sorteio dos Temas da Didática - 3º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 15:00  
03/10/2020 15:40  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Sorteio dos Temas da Didática - 4º Turno (03 candidatos)  
Sorteio dos Temas da Didática - 4º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 15:00  
03/10/2020 19:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Sala de Espera - Prova Didática - 1º Turno (03 candidatos)  
Prova Didática - 1º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 15:00  
03/10/2020 19:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 1º Turno (candidato 1)  
Prova Didática - 1º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 15:00  
03/10/2020 19:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 1º Turno (candidato 2)  
Prova Didática - 1º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 15:00  
03/10/2020 19:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 1º Turno (candidato 3)  
Prova Didática - 1º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 08:00  
03/10/2020 12:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Sala de Espera - Prova Didática - 2º Turno (03 candidatos)  
Prova Didática - 2º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 08:00  
03/10/2020 12:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 2º Turno (candidato 1)  
Prova Didática - 2º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 08:00  
03/10/2020 12:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 2º Turno (candidato 2)  
Prova Didática - 2º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 08:00  
03/10/2020 12:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 2º Turno (candidato 3)  
Prova Didática - 2º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 14:00  
03/10/2020 18:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Sala de Espera - Prova Didática - 3º Turno (03 candidatos)  
Prova Didática - 3º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 14:00  
03/10/2020 18:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 3º Turno (candidato 1)  
Prova Didática - 3º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 14:00  
03/10/2020 18:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 3º Turno (candidato 2)  
Prova Didática - 3º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 14:00  
03/10/2020 18:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 3º Turno (candidato 3)  
Prova Didática - 3º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 15:00  
03/10/2020 19:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Sala de Espera - Prova Didática - 4º Turno (03 candidatos)  
Prova Didática - 4º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 15:00  
03/10/2020 19:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 4º Turno (candidato 1)  
Prova Didática - 4º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 15:00  
03/10/2020 19:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 4º Turno (candidato 2)  
Prova Didática - 4º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
s  
03/10/2020 15:00  
03/10/2020 19:00  
Edital numeroEdital/Ano - SIGLA_SEPARADOR_AREA_CONHECIMENTO_EVENTOS_SIMULTANEOS - Prova Didática - 4º Turno (candidato 3)  
Prova Didática - 4º Turno (03 candidatos) - ÁREA DE CONHECIMENTO DA SIMULAÇÃO  
n  
