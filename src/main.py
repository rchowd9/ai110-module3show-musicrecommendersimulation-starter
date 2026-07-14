"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Render the ranked recommendations in a clean, readable layout."""
    genre = user_prefs.get("preferred_genre") or user_prefs.get("genre", "any")
    mood = user_prefs.get("preferred_mood") or user_prefs.get("mood", "any")

    header = f'Top {len(recommendations)} picks for a "{genre} / {mood}" profile'
    print()
    print(header)
    print("=" * len(header))

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        title = song.get("title", "Unknown title")
        artist = song.get("artist", "Unknown artist")
        print(f"\n#{rank}  {title} ({artist})   score: {score:.2f}")

        # explanation is a "; "-joined string; show each reason on its own line
        reasons = explanation.split("; ") if explanation else []
        for reason in reasons:
            print(f"      - {reason}")
        if not reasons:
            print("      - (no matching attributes)")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Example profile (target_tempo is pre-scaled 0-1; ~115 BPM on a 50-150 range)
    user_prefs = {
        "preferred_genre": "synthwave",
        "preferred_mood": "focused",
        "target_energy": 0.75,
        "target_tempo": 0.65,
        "target_valence": 0.50,
        "target_danceability": 0.60,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
