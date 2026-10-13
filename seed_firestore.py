#!/usr/bin/env python3
"""Seed script for FitPulse Firestore database."""

from google.cloud import firestore

FIRESTORE_PROJECT = "qwiklabs-gcp-04-49c9e2a9e533"

SEEDED_WORKOUTS = [
    {
        "id": "morning-mobility-express",
        "title": "Morning Mobility Express",
        "duration_minutes": 15,
        "difficulty": "beginner",
        "target_area": "full_body",
        "equipment": "none",
        "description": "Gentle morning mobility and dynamic stretching to activate joints and relieve stiffness.",
        "exercises": [
            {"name": "Cat-Cow Stretch", "reps": "10 reps", "cues": "Move smoothly with breathing."},
            {"name": "World's Greatest Stretch", "reps": "5 per side", "cues": "Step lunge, elbow to instep, reach up."},
            {"name": "Bird-Dog", "reps": "10 per side", "cues": "Keep spine neutral, squeeze glute at top."},
            {"name": "Glute Bridges", "reps": "15 reps", "cues": "Drive through heels, pause for 1s at top."}
        ]
    },
    {
        "id": "hiit-bodyweight-burn",
        "title": "Quick HIIT Bodyweight Blast",
        "duration_minutes": 20,
        "difficulty": "intermediate",
        "target_area": "cardio_full_body",
        "equipment": "none",
        "description": "High-intensity interval circuit designed to elevate heart rate and burn maximum calories with zero gear.",
        "exercises": [
            {"name": "Jumping Jacks", "reps": "40s work, 20s rest", "cues": "Light on toes, full overhead clap."},
            {"name": "Bodyweight Squats", "reps": "40s work, 20s rest", "cues": "Chest tall, break parallel."},
            {"name": "Mountain Climbers", "reps": "40s work, 20s rest", "cues": "Hips down, drive knees to chest."},
            {"name": "Plank Shoulder Taps", "reps": "40s work, 20s rest", "cues": "Minimize hip sway, engage core."}
        ]
    },
    {
        "id": "upper-body-dumbbell-sculpt",
        "title": "Upper Body Dumbbell Sculpt",
        "duration_minutes": 25,
        "difficulty": "intermediate",
        "target_area": "upper_body",
        "equipment": "dumbbells",
        "description": "Efficient hypertrophy circuit targeting chest, shoulders, back, and arms using dumbbells.",
        "exercises": [
            {"name": "Dumbbell Floor Press", "reps": "3 sets x 12 reps", "cues": "Elbows at 45-degree angle."},
            {"name": "Bent-Over Dumbbell Rows", "reps": "3 sets x 12 reps", "cues": "Flat back, pull to hip pocket."},
            {"name": "Dumbbell Overhead Shoulder Press", "reps": "3 sets x 10 reps", "cues": "Core tight, press overhead without arching back."},
            {"name": "Hammer Curls to Overhead Triceps Extension", "reps": "3 sets x 12 reps", "cues": "Controlled tempo, elbows pinned."}
        ]
    },
    {
        "id": "lower-body-power-dumbbells",
        "title": "Lower Body Power Circuit",
        "duration_minutes": 25,
        "difficulty": "advanced",
        "target_area": "lower_body",
        "equipment": "dumbbells",
        "description": "Leg and glute builder focusing on strength, balance, and stability.",
        "exercises": [
            {"name": "Goblet Squats", "reps": "4 sets x 12 reps", "cues": "Hold dumbbell at chest, knees track over toes."},
            {"name": "Dumbbell Romanian Deadlifts (RDL)", "reps": "4 sets x 10 reps", "cues": "Hinge at hips, slight knee bend, soft shins."},
            {"name": "Alternating Reverse Lunges", "reps": "3 sets x 10 per leg", "cues": "90-degree angles in both knees."},
            {"name": "Calf Raises", "reps": "3 sets x 20 reps", "cues": "Full extension at top with 2s hold."}
        ]
    },
    {
        "id": "core-abs-igniter",
        "title": "15-Minute Core & Abs Igniter",
        "duration_minutes": 15,
        "difficulty": "beginner",
        "target_area": "core",
        "equipment": "none",
        "description": "Low-impact, spine-friendly core routine strengthening transverse abdominis and obliques.",
        "exercises": [
            {"name": "Forearm Plank", "reps": "3 x 45 seconds", "cues": "Squeeze glutes, push floor away through forearms."},
            {"name": "Deadbugs", "reps": "3 x 10 per side", "cues": "Lower back pressed firmly into the floor."},
            {"name": "Side Plank Hold", "reps": "3 x 30s per side", "cues": "Straight line from shoulders to ankles."},
            {"name": "Bicycle Crunches", "reps": "3 x 15 per side", "cues": "Slow, controlled rotation; don't pull neck."}
        ]
    }
]


def seed_database():
    print(f"Connecting to Firestore in project: {FIRESTORE_PROJECT}")
    db = firestore.Client(project=FIRESTORE_PROJECT)
    collection = db.collection("routines")

    for item in SEEDED_WORKOUTS:
        doc_id = item["id"]
        doc_ref = collection.document(doc_id)
        doc_ref.set(item)
        print(f"  ✓ Seeded routine: {item['title']} (ID: {doc_id})")

    print("\nDatabase seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
