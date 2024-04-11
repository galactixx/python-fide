from pydantic import BaseModel
from pydantic_core import PydanticUndefinedType

def assign_default_if_none(model: BaseModel) -> None:
    """
    """
    for field_name, field_info in model.model_fields.items():
        field_value = getattr(model, field_name)
        if field_value is None:
            if not isinstance(
                field_info.default, PydanticUndefinedType
            ):
                setattr(
                    model, field_name, field_info.default
                )