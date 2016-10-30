from marshmallow import Schema, fields


class MessageSchema(Schema):
    '''
    Message schema for serialization
    '''

    sender_id = fields.Integer()
    receiver_id = fields.Integer()
    text = fields.String()
    status = fields.Integer()
