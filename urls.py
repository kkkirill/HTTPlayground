from views import login, logout, get_form, process_form

urls = {
    '/auth/login': login,
    '/auth/logout': logout,
    '/form': get_form,
    '/charge': process_form
}
