from marshmallow import Schema, fields


class MutualUserSchema(Schema):
    phone_number = fields.String()
    gender = fields.Integer()


class PendingUserSchema(Schema):
    gender = fields.Integer()


class PendingMessageSchema(Schema):
    '''
    Message schema for serialization
    '''

    text = fields.String()
    sending_user = fields.Nested(PendingUserSchema)


class MutualMessageSchema(Schema):
    sender = fields.Nested(MutualUserSchema)
    text = fields.String()
