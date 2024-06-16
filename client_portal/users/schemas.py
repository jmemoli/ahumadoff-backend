from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError
)

from client_portal.users import constants


class CreateUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    name = fields.Str(required=True)

    @validates_schema
    def validate_create_user(self, in_data, **kwargs):
        if 'username' in in_data:
            if len(in_data['username']) < 3:
                raise ValidationError(constants.INVALID_USERNAME)
        if 'password' in in_data:
            if len(in_data['password']) < 3:
                raise ValidationError(constants.INVALID_PASSWORD)
        if 'name' in in_data:
            if len(in_data['name']) < 3:
                raise ValidationError(constants.INVALID_NAME)
        return in_data


class UpdateUserSchema(Schema):
    username = fields.Str(required=False)
    password = fields.Str(required=False)
    name = fields.Str(required=False)

    @validates_schema
    def validate_create_user(self, in_data, **kwargs):
        if 'username' in in_data:
            if len(in_data['username']) < 3:
                raise ValidationError(constants.INVALID_USERNAME)
        if 'password' in in_data:
            if len(in_data['password']) < 3:
                raise ValidationError(constants.INVALID_PASSWORD)
        if 'name' in in_data:
            if len(in_data['name']) < 3:
                raise ValidationError(constants.INVALID_NAME)
        return in_data
