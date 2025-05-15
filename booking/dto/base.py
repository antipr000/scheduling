from drf_pydantic import BaseModel


class BaseDTO(BaseModel):
    @classmethod
    def from_dict(cls, data: dict) -> "BaseDTO":
        serializer = cls.drf_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        return cls(**validated_data)
