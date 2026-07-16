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


# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles.
#
# Each one is built to probe a specific weakness in score_song(). Run them and
# watch whether the ranking matches human intuition — where it doesn't, the
# scoring recipe has a blind spot worth discussing.
# ---------------------------------------------------------------------------

# EDGE CASE 1 — "Conflicting mood vs. energy".
# The user asks for a high-energy track (0.95) but a melancholic mood. In the
# data, melancholic songs are the *lowest* energy ones (Winter Sonata, 0.30).
# Genre (+2.0) and mood (+2.0) are flat categorical bonuses that ignore the
# numeric axes entirely, so the low-energy melancholic song should still rocket
# to the top on +4.0 of categorical points despite directly contradicting the
# requested energy. Exposes: categorical bonuses swamp numeric conflict, and the
# two signal families never cross-check each other.
CONFLICTING_MOOD_ENERGY = {
    "preferred_genre": "classical",
    "preferred_mood": "melancholic",
    "target_energy": 0.95,   # "give me something HIGH energy"
    "target_tempo": 0.90,    # ...and fast
    "target_valence": 0.90,  # ...and upbeat/positive
    "target_danceability": 0.90,
}

# EDGE CASE 2 — "The 0.5 free-rider / no categorical anchor".
# Genre and mood are set to values that appear in NO song, so nobody earns the
# +2.0 categorical bonuses and ranking is driven purely by the numeric axes.
# Every numeric target is 0.5 — and because the farthest any 0-1 attribute can
# sit from 0.5 is 0.5, this profile is *guaranteed* at least half-credit on
# every axis for every song. Nothing is truly "preferred," yet scores stay
# comfortably positive. Exposes: 0.5 is a similarity safe zone that games the
# tie-breakers, and unmatched categoricals fail silently (no signal, no error).
NEUTRAL_FREE_RIDER = {
    "preferred_genre": "polka",     # not present in songs.csv
    "preferred_mood": "existential",  # not present in songs.csv
    "target_energy": 0.50,
    "target_tempo": 0.50,
    "target_valence": 0.50,
    "target_danceability": 0.50,
}

# EDGE CASE 3 — "Out-of-range / malformed input".
# The numeric targets are outside the assumed 0-1 range. _similarity() is
# 1.0 - abs(pref - attr) with no clamping or validation, so these produce
# NEGATIVE point contributions that can drag a genuine genre+mood match below a
# song that matches nothing. The genre also carries a trailing space ("pop ")
# to show that matching is case-insensitive but NOT trimmed, so this "pop" fan
# silently earns zero genre credit. Exposes: no input validation, unbounded
# negative similarity, and brittle exact-string categorical matching.
MALFORMED_INPUT = {
    "preferred_genre": "pop ",     # trailing space -> never matches "pop"
    "preferred_mood": "happy",
    "target_energy": 2.0,          # out of range -> negative similarity
    "target_tempo": -1.0,          # out of range -> negative similarity
    "target_valence": 5.0,         # wildly out of range
    "target_danceability": 0.60,   # the one sane value
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        ("Conflicting mood vs. energy", CONFLICTING_MOOD_ENERGY),
        ("0.5 free-rider / no categorical anchor", NEUTRAL_FREE_RIDER),
        ("Out-of-range / malformed input", MALFORMED_INPUT),
    ]

    for label, user_prefs in profiles:
        print(f"\n########## EDGE CASE: {label} ##########")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
