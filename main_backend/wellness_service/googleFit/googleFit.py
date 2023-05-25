from main_backend.wellness_service.googleFit.app import app
import webbrowser
import threading
import signal

class GoogleFit:
    def __init__(self):
        return
    def auto_googlefit(self, googleFit):
        def open_browser():
            url = "http://127.0.0.1:5000/login"
            webbrowser.open(url, new=1)

        def handler(signum, frame):
            raise Exception("Time is up!")

        # установка обработчика сигнала SIGALRM
        signal.signal(signal.SIGALRM, handler)
        # запуск таймера на 10 секунд
        if __name__ == '__main__':
            threading.Timer(1.25, open_browser).start()
            signal.alarm(10)
            try:
                # выполнение вашего метода
                app.run()
                # отмена таймера
                signal.alarm(0)
            except Exception as e:
                # проверка на прерывание таймером
                if str(e) == "Time is up!":
                    print("Время истекло!")
                else:
                    print("Произошла ошибка:", str(e))

    auto_googlefit(123)