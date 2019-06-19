
from marshmallow import Schema, fields, ValidationError
from pytest import raises

from src.resources.schemas.typed_object_schema import TypedObjectSchema, SerializationContext

class AssertingCallable:

    def __init__(self, expected_kwargs):
        self.__expected_kwargs = expected_kwargs

    def check(self, **actual_kwargs):
        assert actual_kwargs == self.__expected_kwargs

class TestTypedObjectSchema:

    def test_fields_are_combined(self):
        MainSchema = type('MainSchema', (Schema,), {
            "main_field": fields.String(required=True)
        })
        SecondarySchema = type('SecondarySchema', (Schema,), {
            "secondary_field": fields.String()
        })

        assertingCallable = AssertingCallable({"main_field":"main_value", "secondary_field":"secondary_value"})

        serializer = TypedObjectSchema(MainSchema(), [
            SerializationContext("secondary", SecondarySchema(),AssertingCallable,assertingCallable.check)
        ], strict=True)

        serializer.load({
            "main_field" : "main_value",
            "secondary_field" : "secondary_value",
            "type" : "secondary"
        })

    def test_no_failure_if_optional_field_missing(self):
        MainSchema = type('MainSchema', (Schema,), {
            "main_field": fields.String(required=True)
        })
        SecondarySchema = type('SecondarySchema', (Schema,), {
            "secondary_field": fields.String()
        })

        assertingCallable = AssertingCallable({"main_field": "main_value"})

        serializer = TypedObjectSchema(MainSchema(), [SerializationContext("secondary", SecondarySchema(),None, assertingCallable.check)], strict=True)

        serializer.load({
            "main_field" : "main_value",
            "type": "secondary"
        })

    def test_failure_if_missing_mandatory_field_from_main(self):
        MainSchema = type('MainSchema', (Schema,), {
            "main_field": fields.String(required=True)
        })
        SecondarySchema = type('SecondarySchema', (Schema,), {
            "secondary_field": fields.String()
        })

        serializer = TypedObjectSchema(MainSchema(), [SerializationContext("secondary", SecondarySchema(),None, None)], strict=True)

        with raises(ValidationError) as e:
            serializer.load({
                "secondary_field": "secondary_value",
                "type": "secondary"
            })
        assert "main_field" in str(e)

    def test_failure_if_missing_mandatory_field_from_secondary(self):
        MainSchema = type('MainSchema', (Schema,), {
            "main_field": fields.String(required=True)
        })
        SecondarySchema = type('SecondarySchema', (Schema,), {
            "secondary_field": fields.String(required=True)
        })

        serializer = TypedObjectSchema(MainSchema(), [SerializationContext("secondary", SecondarySchema(),None,None)], strict=True)

        with raises(ValidationError) as e:
            serializer.load({
                "main_field" : "main_value",
                "type": "secondary"
            })
        assert "secondary_field" in str(e)

    def test_secondary_overrides_optional_field(self):
        MainSchema = type('MainSchema', (Schema,), {
            "main_field": fields.String(required=True),
            "overridable_field" : fields.String()
        })
        SecondarySchema = type('SecondarySchema', (Schema,), {
            "secondary_field": fields.String(required=True),
            "overridable_field": fields.String(required=True)
        })

        serializer = TypedObjectSchema(MainSchema(), [SerializationContext("secondary", SecondarySchema(), None, None)], strict=True)

        with raises(ValidationError) as e:
            serializer.load({
                "main_field" : "main_value",
                "secondary_field" : "secondary_value",
                "type": "secondary"
            })
        assert "overridable_field" in str(e)

    def test_secondary_does_not_override_mandatory_field(self):
        MainSchema = type('MainSchema', (Schema,), {
            "main_field": fields.String(required=True),
            "overridable_field" : fields.String(required=True)
        })
        SecondarySchema = type('SecondarySchema', (Schema,), {
            "secondary_field": fields.String(required=True),
            "overridable_field": fields.String()
        })

        serializer = TypedObjectSchema(MainSchema(), [SerializationContext("secondary", SecondarySchema(), None, None)], strict=True)

        with raises(ValidationError) as e:
            serializer.load({
                "main_field" : "main_value",
                "secondary_field" : "secondary_value",
                "type": "secondary"
            })
        assert "overridable_field" in str(e)

    def test_serialization(self):
        MainSchema = type('MainSchema', (Schema,), {
            "main_field": fields.String(required=True)
        })
        SecondarySchema = type('SecondarySchema', (Schema,), {
            "secondary_field": fields.String(required=True)
        })

        Value = type('Value', (object, ), {
            "main_field": "main_value",
            "secondary_field": "secondary_value"
        })

        serializer = TypedObjectSchema(MainSchema(), [SerializationContext("secondary", SecondarySchema(), Value, None)],
                                       strict=True)

        value = Value()

        after_serialization = serializer.dump(value)

        assert "type" in after_serialization.data

    def test_serialization_of_unknown_class_fails(self):
        MainSchema = type('MainSchema', (Schema,), {
            "main_field": fields.String(required=True)
        })
        SecondarySchema = type('SecondarySchema', (Schema,), {
            "secondary_field": fields.String(required=True)
        })

        serializer = TypedObjectSchema(MainSchema(), [SerializationContext("secondary", SecondarySchema(), list, None)],
                                       strict=True)

        value = {}

        with raises(ValidationError) as e:
            serializer.dump(value)

        assert "is not configured to deserialize" in str(e)




