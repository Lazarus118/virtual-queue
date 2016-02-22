import twilio
import twilio.rest


class Notify(object):
    def __init__(self, account_sid, auth_token, phone_number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.phone_number = phone_number

    def _request(self, to_number, message):
        try:
            client = twilio.rest.TwilioRestClient(self.account_sid, self.auth_token)
            message = client.messages.create(
                body=message,
                to=to_number,
                from_=self.phone_number
            )
        except twilio.TwilioRestException as e:
            print e

    def send_message(self, to_number, message):
        return self._request(to_number, message)



