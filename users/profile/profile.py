from auth.service import service_gmail


def getprofile():
    response = service_gmail.users().getProfile(userId='me').execute()
    return response