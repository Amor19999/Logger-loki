from marshmallow import Schema, fields, validate


class PageViewList(Schema):
    id = fields.Str()

class LogDetail(Schema):
    id = fields.Str()

class ServiceContext(Schema):
    # ToDo
    # Take a look at marshmallow data validation
    # And add required=True, min/max,regex andetc
    service = fields.Str()
    version = fields.Str()
    msg_id = fields.Str()
    sourceReference = fields.Dict()

class LogCreate(Schema):
    # ToDo
    # Take a look at marshmallow data validation
    # And add required=True, min/max,regex andetc
    time = fields.DateTime()
    message = fields.Str()
    severity = fields.Str()
    error = fields.Str()
    component = fields.Str()
    caller = fields.List(fields.Dict())
    data = fields.Dict()
    stack = fields.List(fields.Dict())
    serviceContext = fields.Nested(ServiceContext)
