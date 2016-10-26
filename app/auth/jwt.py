import jwt
import json

from config import Config


def jwt_required(handler_class):

    def wrap_handler_execute(handler_execute):

        def handle_invalid_jwt(handler):
            handler._transforms = []
            handler.set_status(401)
            handler.write(json.dumps({'error': 'Invalid JWT authentication'}))
            handler.finish()

        def require_auth(handler, kwargs):
            auth = handler.request.headers.get('Authorization')
            if auth:
                parts = auth.split()
                if len(parts) == 2 and parts[0] == 'JWT' and len(parts[1]) > 0:
                    # Token may be in correct format, try to decode it
                    try:
                        payload = jwt.decode(parts[1], Config.JWT['secret'], algorithms=['HS256'])

                        # set an attribute on the handler so we can access the user id later
                        handler.tbh_user_id = payload['user']
                    except:
                        handle_invalid_jwt(handler)
                else:
                    # Token is in incorrect format
                    handle_invalid_jwt(handler)
            else:
                # No authorization given
                handle_invalid_jwt(handler)

            return True

        def _execute(self, transforms, *args, **kwargs):
            try:
                require_auth(self, kwargs)
            except Exception as e:
                print(e)
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute =  wrap_handler_execute(handler_class._execute)
    return handler_class
