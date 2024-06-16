from marshmallow import (
    Schema,
    fields,
)


class UpdateProductSchema(Schema):
    name = fields.Str(required=False)
    base_price = fields.Decimal(required=False)
    description = fields.Str(required=False)


class CreateProductSchema(Schema):
    name = fields.Str(required=True)
    base_price = fields.Decimal(required=True)
    description = fields.Str(required=True)


class CreateProductVariantSchema(Schema):
    product_id = fields.Integer(required=True)
    price = fields.Decimal(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)


class UpdateProductVariantSchema(Schema):
    price = fields.Decimal(required=False)
    name = fields.Str(required=False)
    description = fields.Str(required=False)
