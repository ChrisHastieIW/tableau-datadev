
# # Function to authenticate with Tableau Server REST API using a Personal Access Token
# # and execute a simple command

def pat_tableau_authentication(
    tableau_token_value = '',
    tableau_token_name = 'datadev',
    tableau_content_url = 'chrishastieiwdev598367'
) :
    import tableauserverclient as tsc
    import getpass

    # Request user password if not provided already
    if sfPswd == '' :
        import getpass
        sfPswd = getpass.getpass('Password:')

    tableau_auth = tsc.PersonalAccessTokenAuth(tableau_token_name, tableau_token_value, tableau_content_url)
    server = tsc.Server('https://10ax.online.tableau.com/')

    with server.auth.sign_in(tableau_auth):
        all_wb, pagination_item = server.workbooks.get()
        print("\nThere are {} workbooks on site: ".format(pagination_item.total_available))
        for wb in all_wb:
            print(wb.id, wb.name)
