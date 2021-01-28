
# # Script to automatically create a set of users in Tableau server

# ## This script creates a function which creates users in Tableau server
# ## by leveraging the Tableau REST API and TableauServerClient Python package

def check_if_user_exists(
    server,
    name
) :
    options = tsc.RequestOptions()
    options.filter.add(
        tsc.Filter(
            tsc.RequestOptions.Field.Name,
            tsc.RequestOptions.Operator.Equals,
            name
            )
        )
    filtered_users, _ = server.users.get(req_options = options)

    # Result can either be a matching group or an empty list
    if filtered_users:
        return filtered_users[0]
    else:
        return

def check_if_group_exists(
    server,
    group_name
) :
    options = tsc.RequestOptions()
    options.filter.add(
        tsc.Filter(
            tsc.RequestOptions.Field.Name,
            tsc.RequestOptions.Operator.Equals,
            group_name
            )
        )
    filtered_groups, _ = server.groups.get(req_options = options)

    # Result can either be a matching group or an empty list
    if filtered_groups:
        return filtered_groups[0]
    else:
        return

def automatically_create_users(
    users_to_import,
    tableau_token_value = '',
    tableau_token_name = 'datadev',
    tableau_content_url = 'chrishastieiwdev598367'
) :
    import tableauserverclient as tsc
    import getpass

    # Request user password if not provided already
    if tableau_token_value == '' :
        import getpass
        tableau_token_value = getpass.getpass('Access token:')

    tableau_auth = tsc.PersonalAccessTokenAuth(tableau_token_name, tableau_token_value, tableau_content_url)
    server = tsc.Server('https://10ax.online.tableau.com/', use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        for user in users_to_import:
            group_item = check_if_group_exists(server, user['group'])
            if not group_item :
                new_group = tsc.GroupItem(user['group'])
                group_item = server.groups.create(new_group)

            user_item = check_if_user_exists(server, user['email'])
            if not user_item :
                new_user = tsc.UserItem(user['email'], 'Unlicensed')
                user_item = server.users.add(new_user)

            server.groups.add_user(group_item, user_item.id)

users_to_import = [
    {
        "email": "gzanolli@tableau.com",
        "group": "Developer Relations"
    },
    {
        "email": "developerprogram@tableau.com",
        "group": "Developer Program"
    },
    {
        "email": "jpeach@tableau.com",
        "group": "Developer Marketing"
    }
]

automatically_create_users(
    users_to_import,
    tableau_token_value = '',
    tableau_token_name = 'datadev',
    tableau_content_url = 'chrishastieiwdev598367'
)
