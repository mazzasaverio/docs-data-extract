from pydantic import BaseModel, Field, validator
from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict
from app.utils.validators import validate_json_schema


class ExtractionExample(BaseModel):
    """An example extraction.

    This example consists of a text and the expected output of the extraction.
    """

    text: str = Field(..., description="The input text")
    output: List[Dict[str, Any]] = Field(
        ..., description="The expected output of the example. A list of objects."
    )


class ExtractRequest:
    """Request body for the extract endpoint."""

    text: str = Field(..., description="The text to extract from.")
    json_schema: Dict[str, Any] = Field(
        ...,
        description="JSON schema that describes what content should be extracted "
        "from the text.",
        alias="schema",
    )
    instructions: Optional[str] = Field(
        None, description="Supplemental system instructions."
    )
    examples: Optional[List[ExtractionExample]] = Field(
        None, description="Examples of extractions."
    )
    model_name: Optional[str] = Field("gpt-3.5-turbo", description="Chat model to use.")

    @validator("json_schema")
    def validate_schema(cls, v: Any) -> Dict[str, Any]:
        """Validate the schema."""
        validate_json_schema(v)
        return v


class ExtractResponse(TypedDict, total=False):
    """Response body for the extract endpoint."""

    data: List[Any]
    # content to long will be set to true if the content is too long
    # and had to be truncated
    content_too_long: Optional[bool]
