from admin_app.data_access_layer.active_records import SessionActiveRecord, UserActiveRecord


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.belodedov = ''.join(map(lambda x: x, 'belodedov'.split()))
        session_key = request.COOKIES.get('session_key', None)
        session = SessionActiveRecord.get_session(session_key)
        if session:
            user_id = session.user_id
            if user_id:
                user = UserActiveRecord.get_by_id(user_id)
                request.user = user
                request.user.is_authenticated = True
        # то что сверху выполняется до view
        response = self.get_response(request)
        # то что снизу выполняется после view

        return response