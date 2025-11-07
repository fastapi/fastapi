from datetime import datetime

def health_status() -> dict:
    """
    Returns a simple health status for FastAPI.
    This is a small helper function that could be used in health checks.
    """
    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z"
    }


if __name__ == "__main__":
    print(health_status())
