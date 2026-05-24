from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        user = self.context.get("user")
        validated_data["updated_by"] = user
        return super().update(instance, validated_data)

    def create(self, validated_data):
        user = self.context.get("user")
        validated_data["created_by"] = user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not hasattr(self.Meta, "serialize_fields"):
            return representation

        serialize_fields = self.Meta.serialize_fields
        for field, serializer_class in serialize_fields.items():
            if not hasattr(instance, field):
                continue

            field_value = getattr(instance, field)
            if field_value is None:
                continue

            if hasattr(field_value, "all") and callable(field_value.all):
                # for o2m or m2m relation
                representation[field] = serializer_class(
                    field_value.all(), many=True, context=self.context
                ).data
            else:
                representation[field] = serializer_class(
                    field_value, context=self.context
                ).data

        return representation
