
import yaml
from typing import Dict, Any
from app.schemas.extraction_schema import ExtractRequest
from app.services.extraction import extractor


def create_extraction_request(text: str, config_file_path: str) -> Dict[str, Any]:
   
    # Read the extraction configuration from the YAML file
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)

    # Create the ExtractRequest object
    extraction_request = ExtractRequest(
        text=text,
        json_schema=config['json_schema'],
        instructions=config['instructions'],
        examples=config['examples'],
        model_name=config['model_name']
    )

    # Convert the ExtractRequest object to a dictionary
    extraction_request_dict = extraction_request.dict()


    return extraction_request_dict

async def process_extraction_request(pdf_file_path: str, config_file_path: str) -> ExtractResponse:
    # Create the extraction request
    extraction_request_dict = create_extraction_request(pdf_file_path, config_file_path)

    # Call the extractor function
    extraction_response = await extractor(ExtractRequest(**extraction_request_dict))

    return extraction_response



if __name__ == "__main__":
 
    text = 
    config_file_path = "backend/app/config/extraction_config.yml"
    
    extraction_response = asyncio.run(process_extraction_request(text, config_file_path))
    print(extraction_response)

