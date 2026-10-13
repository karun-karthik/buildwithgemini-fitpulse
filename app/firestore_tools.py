"""Firestore database helper and tools for FitPulse."""

import datetime
from typing import Any, Dict, List, Optional
from google.cloud import firestore

# Important: Hardcode the project ID as a string.
# On Agent Platform, os.getenv("GOOGLE_CLOUD_PROJECT") or google.auth.default() returns
# the project NUMBER instead of the ID, which causes Firestore to fail to locate (default).
FIRESTORE_PROJECT = "qwiklabs-gcp-04-49c9e2a9e533"

_db: Optional[firestore.Client] = None


def get_firestore_client() -> firestore.Client:
    """Return a cached or new Firestore client pinned to FIRESTORE_PROJECT."""
    global _db
    if _db is None:
        _db = firestore.Client(project=FIRESTORE_PROJECT)
    return _db


def search_workout_routines(
    target_area: Optional[str] = None,
    equipment: Optional[str] = None,
    max_duration: Optional[int] = None,
    difficulty: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search available workout routines from the database based on criteria.

    Args:
        target_area: Muscle group or focus (e.g. 'full_body', 'upper_body', 'lower_body', 'core', 'cardio_full_body').
        equipment: Equipment required (e.g. 'none', 'dumbbells', 'resistance_bands').
        max_duration: Maximum duration in minutes (e.g. 15, 20, 30).
        difficulty: Difficulty level ('beginner', 'intermediate', 'advanced').

    Returns:
        A list of matching workout routines with their exercises and instructions.
    """
    db = get_firestore_client()
    docs = db.collection("routines").stream()

    results = []
    for doc in docs:
        data = doc.to_dict()
        if not data:
            continue

        if target_area and target_area.lower() not in data.get("target_area", "").lower():
            continue
        if equipment and equipment.lower() != data.get("equipment", "").lower():
            continue
        if max_duration and data.get("duration_minutes", 0) > max_duration:
            continue
        if difficulty and difficulty.lower() != data.get("difficulty", "").lower():
            continue

        results.append(data)

    return results


def log_completed_workout(
    routine_id: str,
    user_id: str = "default_user",
    duration_minutes: Optional[int] = None,
    notes: Optional[str] = None,
    perceived_exertion_1_to_10: Optional[int] = None,
) -> Dict[str, Any]:
    """Log a completed workout session to the user's workout history.

    Args:
        routine_id: ID or name of the workout routine completed.
        user_id: Identifier for the user.
        duration_minutes: Duration in minutes the workout took.
        notes: Personal reflection or form notes from the workout.
        perceived_exertion_1_to_10: Difficulty rating from 1 (very light) to 10 (maximum effort).

    Returns:
        A confirmation dictionary including the logged session ID and timestamp.
    """
    db = get_firestore_client()
    now = datetime.datetime.now(datetime.timezone.utc)
    
    log_entry = {
        "user_id": user_id,
        "routine_id": routine_id,
        "completed_at": now.isoformat(),
        "duration_minutes": duration_minutes,
        "notes": notes or "",
        "perceived_exertion": perceived_exertion_1_to_10,
    }

    doc_ref = db.collection("workout_logs").document()
    log_entry["log_id"] = doc_ref.id
    doc_ref.set(log_entry)

    return {
        "status": "success",
        "message": f"Successfully logged workout '{routine_id}'!",
        "log_id": doc_ref.id,
        "completed_at": log_entry["completed_at"],
    }


def get_recent_workout_logs(user_id: str = "default_user", limit: int = 5) -> List[Dict[str, Any]]:
    """Retrieve recent workout history logs for a user.

    Args:
        user_id: Identifier for the user.
        limit: Maximum number of recent workout logs to retrieve.

    Returns:
        List of recent workout log records.
    """
    db = get_firestore_client()
    docs = db.collection("workout_logs").where(filter=firestore.FieldFilter("user_id", "==", user_id)).stream()

    logs = []
    for doc in docs:
        data = doc.to_dict()
        if data:
            logs.append(data)
    
    logs.sort(key=lambda x: x.get("completed_at", ""), reverse=True)
    return logs[:limit]
