from app.conf.flask_jwt import jwt_required, jwt_encode, current_identity, jwt_decode


def getUesrname(token):
    jwt_code_dict = jwt_decode(token)
    return jwt_code_dict['identity']['name']

