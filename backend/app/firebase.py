import base64
import json
import logging

import firebase_admin
from firebase_admin import credentials, firestore_async, storage
from google.cloud.firestore_v1.async_client import AsyncClient
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

_app: Optional[firebase_admin.App] = None


def _initialize_firebase() -> firebase_admin.App:
    global _app
    try:
        _app = firebase_admin.get_app()
        logger.info("Firebase Admin SDK already initialized.")
    except ValueError:
        options = {}
        if settings.firebase_storage_bucket:
            options["storageBucket"] = settings.firebase_storage_bucket
            
        if settings.firebase_service_account_base64:
            raw_bytes = base64.b64decode(settings.firebase_service_account_base64)
            sa_dict = json.loads(raw_bytes)
            cred = credentials.Certificate(sa_dict)
            _app = firebase_admin.initialize_app(cred, options)
            logger.info("Firebase Admin SDK initialized from base64 service account.")
        else:
            # Fall back to Application Default Credentials
            _app = firebase_admin.initialize_app(options=options)
            logger.warning(
                "FIREBASE_SERVICE_ACCOUNT_BASE64 not set — "
                "using Application Default Credentials."
            )
    return _app


def get_firestore_client() -> AsyncClient:
    """Return the async Firestore client. Safe to call multiple times."""
    return firestore_async.client()


# Initialize on module import so startup errors surface immediately.
_initialize_firebase()
