from marshmallow import Schema, fields, validate

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


class HttpRequestSchema(Schema):
    method = fields.Str(required=True, validate=validate.OneOf(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]))
    url = fields.Str(required=True, validate=validate.Length(min=1, max=2048))
    path = fields.Str(required=True, validate=validate.Length(min=1, max=2048))
    host = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    userAgent = fields.Str(required=False, data_key="userAgent", validate=validate.Length(max=512))
    accept = fields.Str(required=False, validate=validate.Length(max=512))
    acceptLanguage = fields.Str(required=False, validate=validate.Length(max=128))
    acceptEncoding = fields.Str(required=False, validate=validate.Length(max=128))
    connection = fields.Str(required=False, validate=validate.Length(max=32))
    upgradeInsecureRequests = fields.Str(required=False, validate=validate.Length(max=16))
    ifModifiedSince = fields.Str(required=False, validate=validate.Length(max=64))
    cacheControl = fields.Str(required=False, validate=validate.Length(max=64))

class PageViewCreate(Schema):
    time = fields.DateTime(required=True)
    httpRequest = fields.Nested(HttpRequestSchema, required=True)