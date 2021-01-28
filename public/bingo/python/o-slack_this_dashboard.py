
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

    # Request user password if not provided already
    if tableau_token_value == '' :
        tableau_token_value = getpass.getpass('Access token:')

    tableau_auth = tsc.PersonalAccessTokenAuth(tableau_token_name, tableau_token_value, tableau_content_url)
    server = tsc.Server('https://10ax.online.tableau.com/', use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        all_view_items, pagination_item = server.views.get()
        view_item = all_view_items[0]

        server.views.populate_image(view_item)

        return view_item.image

def post_image_to_slack(
    slack_oath_token = '',
    file_name = '',
    channels = '#tmp-slack-webhook-testing-playground',
    comment = 'Here\'s my test file :smile:'
) :
    # Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError

    # Request user password if not provided already
    if slack_oath_token == '' :
    slack_oath_token = getpass.getpass('Slack OAuth token:')

    # WebClient insantiates a client that can call API methods
    # When using Bolt, you can use either `app.client` or the `client` passed to listeners.
    client = WebClient(token=slack_oath_token)
    # The name of the file you're going to upload

    try:
        # Call the files.upload method using the WebClient
        # Uploading files requires the `files:write` scope
        result = client.files_upload(
            channels=channels,
            initial_comment=comment,
            file=file_name
        )
        # Log the result
        logger.info(result)

    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))

    # url = "https://slack.com/api/chat.postMessage"
    #
    # payload= json.dumps({"channel": "#tmp-slack-webhook-testing-playground", "text": "Testing"})
    # headers = {
    #   'Authorization': 'Bearer {0}'.format(slack_oath_token),
    #   'Content-Type': 'application/json'
    # }
    #
    # response = requests.request("POST", url, headers=headers, data=payload)
    #
    # ##############################
    #
    # url = "https://slack.com/api/files.upload"
    #
    # payload= {"channels": "#tmp-slack-webhook-testing-playground", "title": "Testing", "file" : view_item.image, "filetype" : "png"}
    # headers = {
    #   'Authorization': 'Bearer {0}'.format(slack_oath_token),
    #   'Content-Type': 'multipart/form-data'
    # }
    #
    # response = requests.request("POST", url, headers=headers, data=payload)
    #
    # response.text

def retrieve_dashboard_image_and_post_to_slack(
    slack_oath_token = '',
    tableau_token_value = '',
    tableau_token_name = 'datadev',
    tableau_content_url = 'chrishastieiwdev598367'
) :
    import tempfile

    view_image = retrieve_dashboard_image(slack_oath_token, tableau_token_value, tableau_token_name, tableau_content_url)

    # create a temporary file using a context manager
    with tempfile.TemporaryFile(suffix='.png') as fp:
        fp.write(view_image)

        post_image_to_slack(slack_oath_token, file_name = fp.name, channels = '#tmp-slack-webhook-testing-playground', comment = 'Here\'s my test file :smile:')


retrieve_dashboard_image_and_post_to_slack(
    slack_oath_token = '',
    tableau_token_value = '',
    tableau_token_name = 'datadev',
    tableau_content_url = 'chrishastieiwdev598367'
)
