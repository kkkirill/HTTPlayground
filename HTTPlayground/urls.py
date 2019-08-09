from HTTPlayground.views import login, logout, get_form, process_form

urls = {
    '/authh/login': login,
    '/authh/logout': logout,
    '/form': get_form,
    '/charge': process_form
}
