from HTTPlayground.views import login, logout, get_form, process_form
from HTTPlayground.settings import IS_MAIN_SERVER

if IS_MAIN_SERVER:
    urls = {
        '/auth/login': login,
        '/auth/logout': logout,
        '/charge': process_form
    }
else:
    urls = {
        '/form': get_form,
    }
