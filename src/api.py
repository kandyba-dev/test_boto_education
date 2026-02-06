import logging

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from settings import settings
from src.services import URLService
from src.utils import is_valid_url

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/shorten")
def shorten(url: str, custom_code: str | None = None, service: URLService = Depends()):
    if not is_valid_url(url):
        logger.error(f"Invalid URL: {url}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL",
        )

    try:
        url_model = service.create(url, custom_code)
    except ValueError:
        logger.error(f"Invalid custom code format")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid custom code format",
        )
    except KeyError:
        logger.error(f"Custom code {url} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Custom code already exists",
        )

    return {"short_url": f"{settings.BASE_URL}/{url_model.code}"}


@router.get("/{code}")
def redirect(code: str, service: URLService = Depends()):
    url_model = service.get_by_code(code)
    if not url_model:
        logger.warning(f"URL not found")
        raise HTTPException(
            status_code=404,
            detail="URL not found",
        )

    return RedirectResponse(url_model.original_url)
