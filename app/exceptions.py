class AppError(Exception):
    def __init__(self, mensagem: str, status_code: int = 400):
        self.mensagem = mensagem
        self.status_code = status_code
        super().__init__(mensagem)


class NaoEncontradoError(AppError):
    def __init__(self, mensagem: str):
        super().__init__(mensagem, status_code=404)


class ConflitoError(AppError):
    def __init__(self, mensagem: str):
        super().__init__(mensagem, status_code=409)