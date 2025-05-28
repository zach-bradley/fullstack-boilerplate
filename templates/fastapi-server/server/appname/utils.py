from sqlalchemy.orm import class_mapper
from collections.abc import Iterable

def model_to_dict(instance, strawberry_type):
    """Converts a SQLAlchemy model instance to a dictionary including only fields present in the Strawberry type,
    and handles nested relationships."""
    
    if instance is None:
        return None

    # Extract fields from SQLAlchemy model
    model_dict = {column.name: getattr(instance, column.name) for column in instance.__mapper__.columns}
    
    # Get fields from the corresponding Strawberry GraphQL type
    strawberry_fields = {field.name for field in strawberry_type.__strawberry_definition__.fields}

    # Keep only the fields that exist in the GraphQL type
    filtered_dict = {key: value for key, value in model_dict.items() if key in strawberry_fields}

    # Handle relationships (nested objects)
    for rel in class_mapper(instance.__class__).relationships:
        if rel.key in strawberry_fields:  # Only process relationships that exist in the GraphQL type
            related_obj = getattr(instance, rel.key)

            if related_obj is None:
                filtered_dict[rel.key] = None
            elif isinstance(related_obj, Iterable) and not isinstance(related_obj, str):
                related_type = strawberry_type.__annotations__.get(rel.key)
                filtered_dict[rel.key] = [model_to_dict(obj, related_type) for obj in related_obj]
            else: 
                related_type = strawberry_type.__annotations__.get(rel.key)
                filtered_dict[rel.key] = model_to_dict(related_obj, related_type)
    return filtered_dict
