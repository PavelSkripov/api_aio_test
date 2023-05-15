from app.api.views import (get_list_users, get_user, create_user, delete_user,
                           update_user, get_list_roles, delete_role,
                           update_role, AuthView)


def setup_routes(app):
    """
        Функция описывает пути запросов.

        :param app: объект Application
        :type app: Application
    """
    app.router.add_get('/api/v1/users', get_list_users)
    app.router.add_get('/api/v1/users/{id}', get_user)
    app.router.add_get('/api/v1/roles', get_list_roles)
    app.router.add_post('/api/v1/users', create_user)
    app.router.add_post('/api/v1/login', AuthView)
    app.router.add_delete('/api/v1/users/{id}', delete_user)
    app.router.add_delete('/api/v1/roles/{id}', delete_role)
    app.router.add_put('/api/v1/users/{id}', update_user)
    app.router.add_put('/api/v1/roles/{id}', update_role)
