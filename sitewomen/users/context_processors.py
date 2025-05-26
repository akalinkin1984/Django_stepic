# создаем шаблонный контекстный процессор для добавления menu в шаблон html
from women.utils import menu


def get_women_context(request): # нужно зарегистрировать в settings->TEMPLATES->OPTIONS->context_processors
    return {'mainmenu': menu} # menu будет автоматически доступно во всех шаблонах html через переменную mainmenu
