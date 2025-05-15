from django.http import HttpResponse
from django.views import View
import yaml
import os
from pathlib import Path


class SwaggerView(View):
    def get(self, request):
        # Get the path to swagger.yaml
        base_dir = Path(__file__).resolve().parent.parent.parent
        swagger_path = base_dir / "swagger.yaml"

        # Read and parse the YAML file
        with open(swagger_path, "r") as file:
            swagger_content = yaml.safe_load(file)

        # Convert back to YAML string
        yaml_content = yaml.dump(swagger_content)

        # Return as YAML content
        response = HttpResponse(yaml_content, content_type="text/yaml")
        response["Content-Disposition"] = "inline; filename=swagger.yaml"
        return response
