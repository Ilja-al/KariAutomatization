from mitmproxy import http
from mitmproxy import ctx

class RequestInterceptor:
    @staticmethod
    def request(flow: http.HTTPFlow) -> None:
        """Метод для перехвата и подмены запросов."""
        if "/ecommerce/client/v2/phone/verify" in flow.request.url and flow.request.method == "POST":
            # Логируем запрос
            ctx.log.info(f"Перехвачен запрос: {flow.request.url}")
            ctx.log.info(f"Тело запроса: {flow.request.get_text()}")

            # Подменяем ответ
            flow.response = http.Response.make(
                200,  # статус код
                b'{"status": "READY_FOR_LOGIN"}',  # тело ответа
                {"Content-Type": "application/json"}  # заголовки
            )
            ctx.log.info("Ответ для /phone/verify подменён на READY_FOR_LOGIN")

# Настроим этот перехватчик
addons = [
    RequestInterceptor()
]
