from app.schemas.extraction_schema import ExtractRequest, ExtractResponse
from typing import Any, Dict

from fastapi import HTTPException
from jsonschema import exceptions
from jsonschema.validators import Draft202012Validator


async def extractor(extraction_request: ExtractRequest) -> ExtractResponse:

    schema = extraction_request.json_schema

    try:
        Draft202012Validator.check_schema(schema)
    except exceptions.ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Invalid schema: {e.message}")

    prompt = _make_prompt_template(
        extraction_request.instructions,
        extraction_request.examples,
        schema["title"],
    )
    model = get_model(extraction_request.model_name)

    extractor = prompt | llm.with_structured_output(
        schema=ExtractionData,
        method="function_calling",
        include_raw=False,
    )

    results = await extractor.ainvoke({"text": extraction_request.text})
