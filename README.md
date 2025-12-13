# This repository contains the Most useful features of pydantic v2 in Python.
| Feature           | Why useful                           |
| ----------------- | ------------------------------------ |
| BeforeValidator  | Transform/clean input before parsing |
| AfterValidator   | Enforce constraints after parsing    |
| PlainSerializer  | Control JSON output shape            |
| field_validator  | Validate specific fields             |
| model_validator  | Validate whole model                 |
| field_serializer | Custom JSON rendering for a field               |
| ConfigDict | ConfigDict is a configuration dictionary you assign to the model_config attribute inside a Pydantic model  
| computed_field   | Add dynamic fields                   |
| core_schema      | Full custom type control             |
| model_rebuild()  | Self-referencing models              |
| Smart Union       | Better type coercion                 |
| Rust-backed engine | Huge performance boost               |

model_dump(): Replaces dict() from Pydantic v1.Returns model data as a Python dict.

model_dump_json(): Replaces json() from v1.Returns serialized JSON string.

model_post_init(): New in Pydantic v2 (replaces __post_init__-style hooks).Runs after model initialization for 
extra processing/validation.

model_validate(): Validates data and returns a model instance.Replaces parse_obj() from v1.

model_copy(): Replaces copy() from v1.Makes shallow or deep copies of the model.


| Feature / Method         | Pydantic v1                   | Pydantic v2    | Notes                          |
| ------------------------ | ----------------------------- |----------------| ------------------------------ |
| Convert model to dict    | model.dict()                  | model_dump()   | v2 replacement                 |
| Convert model to JSON    | model.json()                  | model_dump_json() | v2 replacement                 |
| Validate data into model | parse_obj()                   | model_validate() | v2 replacement                 |
| Copy model               | model.copy()                  | model_copy()   | v2 replacement                 |
| Post-init hook           | __post_init__() (dataclasses) / custom logic | model_post_init() | v2 introduces an official hook |
| BaseModel backend        | Pure Python                   | pydantic-core (Rust) | Huge performance boost         |
| Type validation          | Custom validators             | field_validators | New validator system           |
| Root models              | __root__                      | RootModel      | New root model class           |
| Config                   | class Config:                 | model_config = {} | New config style               |
| ORM mode                 | Config.orm_mode = True        | from_attributes=True | Replaces ORM mode              |
| Optional strict types    | strict=True                   | Allowed but redesigned | Cleaner strict handling        |

@field_validator("field", mode="after")
In Pydantic v2, mode="after" in a @field_validator tells Pydantic when to run the validator 
in the validation lifecycle.Run this validator after the field has already been validated and 
converted to its target type.

Use it when:
You want to normalize a validated value
You need ensured types (e.g., list[str], dict, int)
You depend on relationships between list elements
You want to enforce advanced rules after Pydantic parses data

When to use mode="wrap"?
Use mode="wrap" when you need full control
Validate both before and after conversion
Conditionally bypass Pydantic validation
Transform input before and after validation
Raise custom errors using both raw and final values

| Mode  | Runs When                             | Input Value Type             |
| ----- |---------------------------------------|------------------------------|
| before | Before Pydantic’s validation          | Raw input (could be anything) |
| after | After Pydantic’s validation           | Fully validated, converted type |
| wrap | entire validation process for a field | raw input, validated output  |




ConfigDict is a configuration dictionary you assign to the model_config attribute inside a 
Pydantic model to control:
1. strict mode
2. validation behavior
3. extra fields handling
4. ORM mode
5. alias generation
6. JSON encoding
7. many other settings

''model_rebuild() forces Pydantic to:
Recompute the model’s schema
Resolve forward references
Apply newly added fields, annotations, validators, or serializers
Rebuild the internal pydantic-core model'''

✔ You define models in an order that causes forward-reference errors
✔ You dynamically add fields or annotations
✔ You attach validators after class creation
✔ You import models in circular dependency scenarios


| Config                    | FastAPI Benefit           |
| ------------------------- | ------------------------- |
| `strict`                  | Prevents bad client input |
| `extra=forbid`            | Secure APIs               |
| `extra=allow`             | Flexible payloads         |
| `validate_assignment`     | Safe internal updates     |
| `populate_by_name`        | Frontend compatibility    |
| `frozen`                  | Immutable responses       |
| `from_attributes`         | ORM support               |
| `arbitrary_types_allowed` | Internal DI objects       |
