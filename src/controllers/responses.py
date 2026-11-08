from marshmallow import Schema, ValidationError


def validation_error_response(error: ValidationError):
    return {
        "message": "Dados inválidos",
        "errors": error.messages,
    }, 400


def load_form(schema: type[Schema], form):
    try:
        return schema().load(form), None
    except ValidationError as error:
        return None, validation_error_response(error)
