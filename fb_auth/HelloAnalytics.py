"""A simple example of how to access the Google Analytics API."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
            accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                accountId=account,
                webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')

    return None


def get_results(service, profile_id):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    # return service.data().ga().get(
    #     ids='ga:' + profile_id,
    #     start_date='7daysAgo',
    #     end_date='today',
    #     metrics='ga:sessions').execute()

    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date='7daysAgo',
        end_date='today',
        metrics='ga:visits',
        dimensions='ga:source,ga:keyword',
        sort='-ga:visits',
        filters='ga:medium==organic',
        start_index='1',
        max_results='25').execute()


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def print_results(results):
    # Print data nicely for the user.
    if results:
        print('View (Profile):', results.get('profileInfo').get('profileName'))
        print('Total Sessions:', results.get('rows')[0][0])

    else:
        print('No results found')

    output = "View (Profile):" + results.get('profileInfo').get('profileName') + \
        "\n" + 'Total Sessions:' + results.get('rows')[0][0]
    return output


def main(file_location):
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    key_file_location = file_location

    # Authenticate and construct service.
    service = get_service(
        api_name='analytics',
        api_version='v3',
        scopes=[scope],
        key_file_location=key_file_location)

    profile_id = get_first_profile_id(service)
    # output = print_results(get_results(service, profile_id))
    output = get_results(service, profile_id)
    return output


if __name__ == '__main__':
    main()


dict = {'kind': 'analytics#gaData', 'id': 'https://www.googleapis.com/analytics/v3/data/ga?ids=ga:12156345&dimensions=ga:source,ga:keyword&metrics=ga:visits&sort=-ga:visits&filters=ga:medium%3D%3Dorganic&start-date=7daysAgo&end-date=today&start-index=1&max-results=25', 'query': {'start-date': '7daysAgo', 'end-date': 'today', 'ids': 'ga:12156345', 'dimensions': 'ga:source,ga:keyword', 'metrics': ['ga:visits'], 'sort': ['-ga:visits'], 'filters': 'ga:medium==organic', 'start-index': 1, 'max-results': 25}, 'itemsPerPage': 25, 'totalResults': 21, 'selfLink': 'https://www.googleapis.com/analytics/v3/data/ga?ids=ga:12156345&dimensions=ga:source,ga:keyword&metrics=ga:visits&sort=-ga:visits&filters=ga:medium%3D%3Dorganic&start-date=7daysAgo&end-date=today&start-index=1&max-results=25', 'profileInfo': {'profileId': '12156345', 'accountId': '6014281', 'webPropertyId': 'UA-6014281-2', 'internalWebPropertyId': '11618433', 'profileName': 'www.designmind.com', 'tableId': 'ga:12156345'}, 'containsSampledData': False, 'columnHeaders': [{'name': 'ga:source', 'columnType': 'DIMENSION', 'dataType': 'STRING'}, {
    'name': 'ga:keyword', 'columnType': 'DIMENSION', 'dataType': 'STRING'}, {'name': 'ga:visits', 'columnType': 'METRIC', 'dataType': 'INTEGER'}], 'totalsForAllResults': {'ga:visits': '430'}, 'rows': [['google', '(not provided)', '402'], ['bing', 'power bi dashboard templates', '3'], ['baidu', '(not set)', '2'], ['bing', '(not provided)', '2'], ['bing', 'amazon', '2'], ['bing', 'designmind', '2'], ['bing', 'power bi templates', '2'], ['duckduckgo', '(not set)', '2'], ['bing', 'can you schedule power bi refresh', '1'], ['bing', 'cool things to do with power bi business', '1'], ['bing', 'creating power BI report template', '1'], ['bing', 'download power bi themes', '1'], ['bing', 'how to design power bi reports', '1'], ['bing', 'is there a way to apply formatting across every report in power bi', '1'], ['bing', 'power bi refresh schedule dashboard', '1'], ['bing', 'power bi report templates', '1'], ['bing', 'power bi template', '1'], ['bing', 'powerbi adventureworks standard visuals template', '1'], ['bing', 'powrBI consuktants san francisco', '1'], ['bing', 'refresh schedule power bi', '1'], ['yandex', '(not set)', '1']]}
