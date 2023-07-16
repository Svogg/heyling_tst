import requests


class RequestSender:

    def __init__(self, url):
        self.url = url

    def check_status(self) -> int:
        """
        Метод, проверяющий статус сервиса, к которому подключается
        :return:
        """
        try:
            status = requests.get(url=self.url, timeout=10).status_code
            return status
        except requests.exceptions.Timeout:
            print('The request timed out')
        except requests.exceptions.ConnectionError:
            print('Connection closed')

    def send_message(self):
        """
        Метод, позволяющий отрпавлять post-запросы в сервис
        :return:
        """
        if self.check_status() != 404:
            while True:
                try:
                    message = str(input('Enter the message: '))
                    requests.post(url=self.url + message)
                except KeyboardInterrupt:
                    print('\nSession closed')
                    break
        else:
            print('Невозможно подключиться')


sender = RequestSender('http://127.0.0.1:8000/queue_reverse_text?text=')

sender.send_message()
