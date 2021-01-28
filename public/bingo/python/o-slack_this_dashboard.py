
# # Script to automatically create a set of users in Tableau server

# ## This script creates a function which creates users in Tableau server
# ## by leveraging the Tableau REST API and TableauServerClient Python package

def retrieve_dashboard_image(
    slack_oath_token = '',
    tableau_token_value = '',
    tableau_token_name = 'datadev',
    tableau_content_url = 'chrishastieiwdev598367'
) :
    import tableauserverclient as tsc
    import getpass
    import requests
    import json
    import base64

    # Request user password if not provided already
    if slack_oath_token == '' :
        slack_oath_token = getpass.getpass('Slack OAuth token:')

    # Request user password if not provided already
    if tableau_token_value == '' :
        tableau_token_value = getpass.getpass('Access token:')

    tableau_auth = tsc.PersonalAccessTokenAuth(tableau_token_name, tableau_token_value, tableau_content_url)
    server = tsc.Server('https://10ax.online.tableau.com/', use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        all_view_items, pagination_item = server.views.get()
        view_item = all_view_items[0]
        server.views.populate_csv(view_item)
        server.views.populate_image(view_item)

        with open('./view_image.png', 'wb') as f:
            f.write(view_item.image)

        print(b''.join(view_item.csv).decode("utf-8"))

    url = "https://slack.com/api/chat.postMessage"

    payload= json.dumps({"channel": "#tmp-slack-webhook-testing-playground", "text": "Testing"})
    headers = {
      'Authorization': 'Bearer {0}'.format(slack_oath_token),
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    ##############################

    url = "https://slack.com/api/files.upload"

    payload= {"channels": "#tmp-slack-webhook-testing-playground", "title": "Testing", "file" : view_item.image, "filetype" : "png"}
    headers = {
      'Authorization': 'Bearer {0}'.format(slack_oath_token),
      'Content-Type': 'multipart/form-data'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


retrieve_dashboard_image(
    tableau_token_value = '',
    tableau_token_name = 'datadev',
    tableau_content_url = 'chrishastieiwdev598367'
)
