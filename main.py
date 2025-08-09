import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette_prometheus import metrics, PrometheusMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from api.v1.api import api_router

import os


flower_url = os.getenv("FLOWER_URL", "http://localhost:5555")
broker_url = os.getenv("BROKER_URL", "http://localhost:5672")
grafana_url = os.getenv("GRAFANA_URL", "http://localhost:3000")
insights_url = os.getenv("INSIGHTS_URL", "http://localhost:8555")

tags_metadata = [
  {
      "name": "monitoring",
      "description": "Healthcheck services",
  },
  {
      "name": "deployment",
      "description": "Deployment services",
  }
]

description = f"""
DeployFlow aims to simplify and automate the deployment process for your htmls.

* [Insights]({insights_url})
* [Admin Panel]({flower_url}) 
* [Broker]({broker_url})
* [Grafana]({grafana_url})
"""

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title, 
        version="1.0.0",
        description=description,
        routes=app.routes,
        tags=tags_metadata,
        contact={
            "name": "Cansin Aldanmaz",
            "email": "cansinaldanmaz@gmail.com",
        },
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://static1.srcdn.com/wordpress/wp-content/uploads/thor-hammer-lightning.jpg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    openapi_url=f"/api/v1/openapi.json",
    docs_url=None, 
    redoc_url=None,
    title="DeployFlow"
)
app.openapi = custom_openapi

app.add_middleware(PrometheusMiddleware)
app.add_route("/api/v1/monitoring/metrics", metrics)
app.include_router(api_router, prefix="/api/v1")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)