import abc


class UrlManager:
    @abc.abstractmethod
    def get_url(self, params):
        raise NotImplementedError
