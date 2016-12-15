from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import dropbox

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/tasks-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/tasks.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Dragonfly TODO Manager'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'tasks-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()   
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def parser(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    for i in lines:
    #    print i
        if i.find("todo:") != -1:
            t = i.split()
            t.remove("todo:")
            print (t)
            for j in t:
                if j[0] == "@":
                    print ("People: ", j)
                    t.remove(j)
                if j[0] == "[":
                    print ("Due date: ", j)
                    t.remove(j)
            print (t)

def task_getter():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('tasks', 'v1', http=http)

    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])
    if not items:
        print('No task lists found.')
    else:
        print('Task lists:')
        for item in items:
            # print (type(items))
            # print (item)
            print('{0} ({1})'.format(item['title'], item['id']))
            # print(item['title'], item['id'])

    results_tasks = service.tasks().list(tasklist="@default").execute()
    items = results_tasks.get('items', [])
    print('\nDefault tasks:')
    for item in items:
        # print('{0} ({1})'.format(item['title'], item['id']))
        print(item['title'])

def dbx_getter():
    f = open('dbx_secret', 'r')
    dbx = dropbox.Dropbox(f.readlines()[0])
    f.close()
    # print (dbx.users_get_current_account())
    for entry in dbx.files_list_folder('').entries:
        print("filename:", entry.name)
        # parser(entry.name)

def main():
    #TODO : Main loop here
    dbx_getter()

if __name__ == '__main__':
    main()

