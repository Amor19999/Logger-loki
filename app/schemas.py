from marshmallow import Schema, fields


class PageViewList(Schema):
    id = fields.Str()

class LogDetail(Schema):
    id = fields.Str()

class ServiceContext(Schema):
    # ToDo
    # Take a look at marshmallow data validation
    # And add required=True, min/max,regex andetc
    service_name = fields.Str()
    version = fields.Str()
    httpRequest = fields.Dict()
    sourceReference = fields.Dict()
    user = fields.Str(allow_none=True)
    request_id = fields.Str(allow_none=True)

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


