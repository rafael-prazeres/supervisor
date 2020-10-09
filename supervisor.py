##########################################################################################################
#                                                                                                        #
#   PROPOSTA DO SCRIPT: construir, de forma colaborativa, uma ferramenta                                 #
#   de apoio às atividades do supervisor de gravação de prova didática da UFRN                           #
#   que possibilite:                                                                                     #
#                                                                                                        #
# * Automatizar o processo de criação no Google Drive, bem como autorização de acesso,                   #
#   das pastas indicadas nas instruções encaminhadas pela comissão organizadora de concursos.            #
#                                                                                                        #
# * Automatizar o processo de criação de eventos no Calendário do Google,                                #
#   indicação de convidados e criação de sala de videochamada,                                           #
#   conforme cronograma recebido pela comissão examinadora/secretaria da cada departamento/UAE           #
#                                                                                                        #
#   Fontes:                                                                                              #
# * https://developers.google.com/drive/api/v3/quickstart/python                                         #
# * https://karenapp.io/articles/how-to-automate-google-calendar-with-python-using-the-calendar-api/     #
# * https://developers.google.com/calendar/v3/reference/events/insert                                    #
#                                                                                                        #
##########################################################################################################

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
from datetime import datetime as datetime2, timedelta
import sys

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/calendar']

def search_folder(drive_service, folder_name, folder_id):

    ''' Procura uma pasta no drive e retorna o seu id  '''

    page_token = None
    while True:
        if not folder_id:
            response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='%s'" % folder_name,
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, webViewLink, name)',
                                                  pageToken=page_token).execute()
        else:
            response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='%s' and '%s' in parents" % (folder_name, folder_id),
                                              spaces='drive',
                                              fields='nextPageToken, files(id, webViewLink, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            print(file.get('webViewLink') + " <- Link da pasta "+ folder_name)
            return file.get('id')
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

def create_folder(drive_service, folder_name, folder_id):

    ''' Cria uma pasta no drive e retorna o seu id  '''

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    if folder_id:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id]
        }

    
    file = drive_service.files().create(body=file_metadata,fields='id, webViewLink').execute()
    print(file.get('webViewLink') + " <- Link da pasta "+ folder_name)
    return file.get('id')

def obter_entradas():

    '''Lê entradas do usuário e retorna uma lista com os valores'''
    
    print("Seja Bem-vindo Supervisor de Prova Didática!")
    print()
    edital = input("Informe o número/ano do edital: ")
    print()
    area_conhecimento = input("Informe o nome da área de conhecimento: ")
    print()
    sigla_area_conhecimento = input("Informe uma sigla para facilitar a distinção entre eventos simultâneos na agenda: ")
    print()
    qtd_turnos = int(input('informe a quantidade de turnos necessários: '))
    print()
    qtd_candidatos_turno = int(input('informe a quantidade de candidatos por turno: '))
    print()

    return [edital, area_conhecimento, sigla_area_conhecimento, qtd_turnos, qtd_candidatos_turno]

def criar_pastas_prova_didatica(service, area_conhecimento_folder_id, qtd_turnos, qtd_candidatos_turno): 

    '''Caso não exista, cria tabela de pastas conforme orientações da comissão organizadora de concursos'''
    
    pastas_sem_permissoes = []
    sorteios_folder_id = search_folder(service, 'Sorteios de Ordem e Temas da Didática', area_conhecimento_folder_id)
    atas_folder_id = search_folder(service, 'Atas', area_conhecimento_folder_id)
    fichas_folder_id = search_folder(service, 'Fichas de Avaliação', area_conhecimento_folder_id)
    apresentacoes_folder_id = search_folder(service, 'Apresentações da Prova Didática', area_conhecimento_folder_id)
    resultado_folder_id = search_folder(service, 'Divulgação do resultado (NFC)', area_conhecimento_folder_id)

    if not sorteios_folder_id:
        sorteios_folder_id = create_folder(service, 'Sorteios de Ordem e Temas da Didática', area_conhecimento_folder_id)
    pastas_sem_permissoes.append(sorteios_folder_id)

    if not atas_folder_id:
        atas_folder_id = create_folder(service, 'Atas', area_conhecimento_folder_id)
    pastas_sem_permissoes.append(atas_folder_id)

    if not fichas_folder_id:
        fichas_folder_id = create_folder(service, 'Fichas de Avaliação', area_conhecimento_folder_id)
    pastas_sem_permissoes.append(fichas_folder_id)

    if not apresentacoes_folder_id:
        apresentacoes_folder_id = create_folder(service, 'Apresentações da Prova Didática', area_conhecimento_folder_id)
    pastas_sem_permissoes.append(apresentacoes_folder_id)

    if not resultado_folder_id:
        resultado_folder_id = create_folder(service, 'Divulgação do resultado (NFC)', area_conhecimento_folder_id)
    pastas_sem_permissoes.append(resultado_folder_id)

    aux = 1
    while aux <= qtd_turnos:
        turno_folder_id = search_folder(service, 'Prova Didática - %sº Turno (%s candidatos)' % (aux, qtd_candidatos_turno), area_conhecimento_folder_id)
        if not turno_folder_id:
            turno_folder_id = create_folder(service, 'Prova Didática - %sº Turno (%s candidatos)' % (aux, qtd_candidatos_turno), area_conhecimento_folder_id)
        pastas_sem_permissoes.append(turno_folder_id)
        turno_folder_id = None
        aux = aux + 1

    aux = 1
    while aux <= qtd_turnos:
        turno_folder_id = search_folder(service, 'Entrega eletrônica do plano de aula (formato PDF) - %sº Turno (%s candidatos)' % (aux, qtd_candidatos_turno), area_conhecimento_folder_id)
        if not turno_folder_id:
            turno_folder_id = create_folder(service, 'Entrega eletrônica do plano de aula (formato PDF) - %sº Turno (%s candidatos)' % (aux, qtd_candidatos_turno), area_conhecimento_folder_id)
        pastas_sem_permissoes.append(turno_folder_id)
        turno_folder_id = None
        aux = aux + 1

    return pastas_sem_permissoes

def le_emails(nome_papel):

    '''A funcao lê os emails a serem utilizados no processo de autorização de acesso 
       às pastas e devolve uma lista contendo cada email como um elemento'''

    i = 1
    emails = []
    email = input("Informe o email do " + str(i) + "º " + nome_papel + " (aperte enter para sair): ")
    while email:
        emails.append(email)
        i += 1
        email = input("Informe o email do " + str(i) + "º " + nome_papel + " (aperte enter para sair): ")

    return emails

def callback(request_id, response, exception):

    ''' Usada na execução de requisições em lote à api do google   '''

    if exception:
        # Handle error
        print (exception)
    else:
        print ("Permission Id: %s" % response.get('id'))

def autorizar_contas(emails_comissao, folder_id, batch, drive_service, role):

    ''' Compartilha um arquivo/pasta do drive com uma lista de contas do goole  '''

    for email in emails_comissao:
        user_permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        batch.add(drive_service.permissions().create(
            fileId=folder_id,
            body=user_permission,
            sendNotificationEmail=False,
            fields='id',
        ))

    return batch

def autorizar_conta(email, folder_id, batch, drive_service, role):

    ''' Compartilha um arquivo/pasta do drive com uma conta do goole  '''

    user_permission = {
        'type': 'user',
        'role': role,
        'emailAddress': email
    }
    batch.add(drive_service.permissions().create(
        fileId=folder_id,
        body=user_permission,
        sendNotificationEmail=False,
        fields='id',
    ))

    return batch

def autorizar_contas_concursos(emails_concursos, pastas_sem_permissoes, batch, service):

    ''' Autoriza a comissão organizadora de concursos, conforme tabela de pastas
        existente nas orientações encaminhadas pela comissão organizadora de concursos '''

    sorteios_folder_id = pastas_sem_permissoes[0]
    atas_folder_id = pastas_sem_permissoes[1]
    resultado_folder_id = pastas_sem_permissoes[4]

    for conta in emails_concursos:
        batch = autorizar_conta(conta, sorteios_folder_id, batch, service,'reader')
        batch = autorizar_conta(conta, atas_folder_id, batch, service,'reader')
        batch = autorizar_conta(conta, resultado_folder_id, batch, service,'reader')
            
    return batch

def autorizar_contas_candidatos(emails_candidatos, pastas_sem_permissoes, batch, service, qtd_turnos):

    ''' Autoriza candidatos do processo seletivo conforme tabela de pastas
        presente nas orientações encaminhadas pela comissão organizadora de concursos '''

    sorteios_folder_id = pastas_sem_permissoes[0]
    atas_folder_id = pastas_sem_permissoes[1]
    resultado_folder_id = pastas_sem_permissoes[4]
    offset_pastas_provas = 5

    for conta in emails_candidatos:
        offset_pastas_entrega = offset_pastas_provas + qtd_turnos
        batch = autorizar_conta(conta, sorteios_folder_id, batch, service,'reader')
        batch = autorizar_conta(conta, atas_folder_id, batch, service,'reader')
        batch = autorizar_conta(conta, resultado_folder_id, batch, service,'reader')
        while offset_pastas_entrega < len(pastas_sem_permissoes):
            batch = autorizar_conta(conta, pastas_sem_permissoes[offset_pastas_entrega], batch, service,'writer')
            offset_pastas_entrega = offset_pastas_entrega + 1

    return batch

def proibir_contas(emails_comissao, folder_id, batch, drive_service, role):

    ''' Remove permissões de acesso de um arquivo/pasta do drive  '''

    for email in emails_comissao:
        user_permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        batch.add(drive_service.permissions().delete(
            fileId=folder_id,
            permissionId=email,
        ))

    return batch

def get_drive_service():

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return service

def processar_lote_permissoes(emails_comissao, emails_supervisores, emails_concursos, emails_candidatos,
                              drive_service, area_conhecimento_folder_id, pastas_sem_permissoes, qtd_turnos, qtd_candidatos_turno):

    batch = drive_service.new_batch_http_request(callback=callback)

    if emails_comissao:
        print()
        print("Autorizando a comissão examinadora...")
        batch = autorizar_contas(emails_comissao, area_conhecimento_folder_id, batch, drive_service, 'writer')
        for email in emails_supervisores:
            print(email)

    
    if emails_supervisores:
        print()
        print("Autorizando os supervisores...")
        batch = autorizar_contas(emails_supervisores, area_conhecimento_folder_id, batch, drive_service, 'writer')
        for email in emails_supervisores:
            print(email)
    
    if emails_concursos:
        print()
        print("Autorizando a comissão organizadora do concurso...")
        if len(pastas_sem_permissoes) > 0:
            batch = autorizar_contas_concursos(emails_concursos, pastas_sem_permissoes, batch, drive_service)
        for email in emails_concursos:
            print(email)
    
    #if emails_candidatos:
    #    print()
    #    print("Autorizando candidatas e candidatos...")
    #    print()
    #    if len(pastas_sem_permissoes) > 0:
    #        batch = autorizar_contas_candidatos(emails_candidatos, pastas_sem_permissoes, batch, drive_service, qtd_turnos)

    batch.execute()

def get_calendar_service():
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def findAllCalendars(calendar_service):
    
    # Call the Calendar API
    print('Getting list of calendars')
    calendars_result = calendar_service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])

    if not calendars:
        print('No calendars found.')
    for calendar in calendars:
        summary = calendar['summary']
        id = calendar['id']
        primary = "Primary" if calendar.get('primary') else ""
        print("%s\t%s\t%s" % (summary, id, primary))

def findNextEvents(calendar_service):

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = calendar_service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=200, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events

def findNextEventsByTextInSummary(calendar_service, text_in_summary):

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = calendar_service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=200, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    found_events = []
    for event in events:
        if text_in_summary in event['summary']:
            found_events.append(event)

    return found_events


def create_event(calendar_service, start, end, sumary, description, emails, batch):

    '''A funcao recebe os dados e cria evento na agenda do google'''

    batch.add(calendar_service.events().insert(calendarId='primary',
                                                    conferenceDataVersion=1,
                                                    sendNotifications=False,
                                                    sendUpdates='none',
                                                    body={
                                                        "attendees": [{'email': x} for x in emails],
                                                        "summary": sumary,
                                                        "description": description,
                                                        "start": {"dateTime": start, "timeZone": 'America/Recife'},
                                                        "end": {"dateTime": end, "timeZone": 'America/Recife'},
                                                        "conferenceData": {
                                                            "createRequest": { "requestId": "supervisorGravacaoProvaUFRN" },
                                                            },
                                                        }
                                                    ))

    return batch

def criar_eventos(calendar_service, emails_convidados):

    '''A funcao solicita entradas e cria eventos eventos na agenda do google'''

    batch = calendar_service.new_batch_http_request(callback=callback)

    i = 1
    eventos = []
    tem_outro = 'n'
    
    inicio = input("Informe o inicio do: " +str(i)+ "º evento: ")
    fim = input("Informe o fim do: " +str(i)+ "º evento: ")

    inicio = datetime.datetime.strptime(inicio, '%d/%m/%Y %H:%M').isoformat()
    fim = datetime.datetime.strptime(fim, '%d/%m/%Y %H:%M').isoformat()
    
    sumario = input("Informe o sumário do: " +str(i)+ "º evento: ")
    descricao = input("Informe a descrição do: " +str(i)+ "º evento: ")
    batch = create_event(calendar_service, inicio, fim, sumario, descricao, emails_convidados, batch)
    tem_outro = input("Tem outro evento (s/n): ")

    while tem_outro == 's':
        i = i + 1
        inicio = input("Informe o inicio do: " + str(i) + "º evento: ")
        fim = input("Informe o fim do: " +str(i)+ "º evento: ")
        
        inicio = datetime.datetime.strptime(inicio, '%d/%m/%Y %H:%M').isoformat()
        fim = datetime.datetime.strptime(fim, '%d/%m/%Y %H:%M').isoformat()
        
        sumario = input("Informe o sumário do: " +str(i)+ "º evento: ")
        descricao = input("Informe a descrição do: " +str(i)+ "º evento: ")
        batch = create_event(calendar_service, inicio, fim, sumario, descricao, emails_convidados, batch)
        tem_outro = input("Tem outro evento (s/n): ")
    
    batch.execute()

def main():

    ''' Início do fluxo de execução '''

    drive_service = get_drive_service()
    
    calendar_service = get_calendar_service()

    entradas = obter_entradas()
    print()

    emails_comissao = le_emails('membro da comissão examinadora')
    print()

    emails_supervisores = le_emails('membro do grupo de supervisores')
    print()

    emails_concursos = le_emails('membro da comissão organizadora de concursos')
    print()

    emails_candidatos = le_emails('do(a) candidato(a)')
    print()

    edital = entradas[0]
    area_conhecimento = entradas[1]
    sigla_area_conhecimento = entradas[2]
    qtd_turnos = entradas[3]
    qtd_candidatos_turno = entradas[4]
    area_conhecimento = area_conhecimento + " - Edital " + edital

    print()
    print("Dados das pastas para preenchimento do cronograma...")
    print()

    edital_folder_id = search_folder(drive_service, edital, None)

    if not edital_folder_id:
        edital_folder_id = create_folder(drive_service, edital, edital_folder_id)
    
    area_conhecimento_folder_id = search_folder(drive_service, area_conhecimento, edital_folder_id)

    if not area_conhecimento_folder_id:
        area_conhecimento_folder_id = create_folder(drive_service, area_conhecimento, edital_folder_id)

    pastas_sem_permissoes = []

    if area_conhecimento_folder_id:
        pastas_sem_permissoes  = criar_pastas_prova_didatica(drive_service, area_conhecimento_folder_id, qtd_turnos, qtd_candidatos_turno)

    print()
    print("Quantidade de pastas criadas: " + str(len(pastas_sem_permissoes)))    

    print()
    print("Inserindo permissões...")

    processar_lote_permissoes(emails_comissao, emails_supervisores, emails_concursos, emails_candidatos,
                              drive_service, area_conhecimento_folder_id, pastas_sem_permissoes, qtd_turnos, qtd_candidatos_turno)
    
    print()
    print("Tabela de pastas criada com sucesso.")
    print()

    emails_examinadores_supervisores = []
    #emails_examinadores_supervisores.extend(emails_comissao)
    emails_examinadores_supervisores.extend(emails_supervisores)
    
    #criar_eventos(calendar_service, emails_examinadores_supervisores)

    eventos = findNextEventsByTextInSummary(calendar_service, sigla_area_conhecimento)

    print("Dados dos Eventos para preenchimento do cronograma:")
    print()
    if not eventos:
        print('No upcoming events found.')
    aux = 0
    for evento in eventos:
        start = evento['start'].get('dateTime', evento['start'].get('date'))
        print("-> ",start, evento['summary'])
        print(evento['conferenceData'].get('entryPoints')[0]['uri'])
        print(evento['conferenceData'].get('entryPoints')[0]['label'])
        print(evento['conferenceData'].get('conferenceSolution')['name'])
        print()
        aux = aux + 1
    print(str(aux) + " eventos criados com sucesso.")
    print()

if __name__ == '__main__':
    main()
