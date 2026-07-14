from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from operator import itemgetter
import csv

# ---------------------------------------------------------------------------
# Scoring weights (the "Algorithm Recipe")
#
#   Genre match  -> +2.0   primary hard filter: get the category right first
#   Mood match   -> +1.0   secondary categorical signal (crosses genres)
#   Energy       -> +0.0 to +1.0  graded similarity, the tie-breaker
#
# Energy similarity is 1 - |song.energy - target_energy|, so a perfect energy
# match is worth as much as a mood match and a distant one still gives a small
# baseline. Drop ENERGY_WEIGHT to 0.5 if you want the two categorical matches
# to clearly dominate ranking.
# ---------------------------------------------------------------------------
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score(
    pref_genre: str,
    pref_mood: str,
    target_energy: float,
    song_genre: str,
    song_mood: str,
    song_energy: float,
) -> Tuple[float, List[str]]:
    """
    Shared scoring core used by both the OOP and functional APIs.

    Returns (score, reasons) where reasons is a list of human-readable
    strings explaining which rules fired and how many points they added.
    """
    score = 0.0
    reasons: List[str] = []

    # +2.0 for a genre match (case-insensitive so "Pop" == "pop")
    if pref_genre and song_genre.lower() == pref_genre.lower():
        score += GENRE_WEIGHT
        reasons.append(f"genre match ({song_genre}, +{GENRE_WEIGHT:.1f})")

    # +1.0 for a mood match
    if pref_mood and song_mood.lower() == pref_mood.lower():
        score += MOOD_WEIGHT
        reasons.append(f"mood match ({song_mood}, +{MOOD_WEIGHT:.1f})")

    # Graded energy similarity: closer to the target => more points
    diff = abs(song_energy - target_energy)
    energy_points = ENERGY_WEIGHT * (1.0 - diff)
    score += energy_points
    closeness = "close" if diff <= 0.15 else "partial" if diff <= 0.35 else "far"
    reasons.append(
        f"energy {closeness} "
        f"({song_energy:.2f} vs target {target_energy:.2f}, +{energy_points:.2f})"
    )

    return score, reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        return _score(
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            song.genre,
            song.mood,
            song.energy,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(
            self.songs,
            key=lambda s: self._score_song(user, s)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score_song(user, song)
        return (
            f"Recommended '{song.title}' by {song.artist} "
            f"(score {score:.2f}): " + "; ".join(reasons)
        )


# Columns cast to int (whole-number identifiers) vs float (0-1 audio features
# and BPM). Anything not listed here — title, artist, genre, mood — stays a
# string. Only columns actually present in the CSV are converted, so optional
# feature columns (instrumentalness, speechiness) don't create phantom keys.
INTEGER_FIELDS = {"id"}
FLOAT_FIELDS = {
    "energy", "tempo_bpm", "valence", "danceability",
    "acousticness", "instrumentalness", "speechiness",
}


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV into a list of dicts, casting id to int and audio features to float."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parsed: Dict = {}
            for key, value in row.items():
                if value is None or value == "":
                    # preserve the column but flag missing numeric data
                    parsed[key] = None if key in INTEGER_FIELDS or key in FLOAT_FIELDS else value
                elif key in INTEGER_FIELDS:
                    parsed[key] = int(value)
                elif key in FLOAT_FIELDS:
                    parsed[key] = float(value)
                else:
                    parsed[key] = value
            songs.append(parsed)
    return songs


# ---------------------------------------------------------------------------
# Custom scoring recipe used by the functional score_song() API.
#
#   genre match             -> +2.0   (flat categorical bonus)
#   mood match              -> +2.0   (flat categorical bonus)
#   energy similarity       -> weight 1.0
#   tempo similarity        -> weight 1.0
#   valence similarity      -> weight 0.5
#   danceability similarity -> weight 0.5
#
# Numeric similarity is 1.0 - |preference - attribute| on a 0-1 axis.
# ---------------------------------------------------------------------------
RECIPE_GENRE_WEIGHT = 2.0
RECIPE_MOOD_WEIGHT = 2.0
NUMERIC_WEIGHTS = {
    "energy": 1.0,
    "tempo": 1.0,
    "valence": 0.5,
    "danceability": 0.5,
}

# tempo_bpm is stored raw (beats per minute) but target_tempo is pre-scaled to
# 0-1, so the song's BPM is scaled onto the same axis before comparison.
# 50-150 BPM is the range for which the profile's "0.65 == ~115 BPM" holds.
TEMPO_MIN_BPM = 50.0
TEMPO_MAX_BPM = 150.0


def _similarity(preference: float, attribute: float) -> float:
    """Graded closeness on a 0-1 axis: 1.0 when equal, lower as they diverge."""
    return 1.0 - abs(preference - attribute)


def _pref(user_prefs: Dict, *keys, default=None):
    """Return the first present, non-None preference among alternative names."""
    for key in keys:
        if user_prefs.get(key) is not None:
            return user_prefs[key]
    return default


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song dict against user prefs via the custom recipe, returning (total_score, reasons)."""
    total_score = 0.0
    reasons: List[str] = []

    # --- Categorical features ---
    pref_genre = _pref(user_prefs, "preferred_genre", "genre", default="")
    if pref_genre and str(song.get("genre", "")).lower() == str(pref_genre).lower():
        total_score += RECIPE_GENRE_WEIGHT
        reasons.append("genre match (+2.0)")

    pref_mood = _pref(user_prefs, "preferred_mood", "mood", default="")
    if pref_mood and str(song.get("mood", "")).lower() == str(pref_mood).lower():
        total_score += RECIPE_MOOD_WEIGHT
        reasons.append("mood match (+2.0)")

    # --- Numerical features: energy, tempo, valence, danceability ---
    # Scale the song's raw BPM onto the same 0-1 axis as target_tempo.
    song_tempo_scaled = None
    raw_tempo = song.get("tempo_bpm")
    if raw_tempo is not None:
        song_tempo_scaled = (float(raw_tempo) - TEMPO_MIN_BPM) / (TEMPO_MAX_BPM - TEMPO_MIN_BPM)
        song_tempo_scaled = max(0.0, min(1.0, song_tempo_scaled))  # clamp to 0-1

    numeric_features = {
        "energy": (_pref(user_prefs, "target_energy", "energy"), song.get("energy")),
        "tempo": (_pref(user_prefs, "target_tempo", "tempo"), song_tempo_scaled),
        "valence": (_pref(user_prefs, "target_valence", "valence"), song.get("valence")),
        "danceability": (
            _pref(user_prefs, "target_danceability", "danceability"),
            song.get("danceability"),
        ),
    }

    for feature, (preference, attribute) in numeric_features.items():
        if preference is None or attribute is None:
            continue  # profile or song doesn't define this feature
        points = NUMERIC_WEIGHTS[feature] * _similarity(float(preference), float(attribute))
        total_score += points
        reasons.append(f"{feature} match (+{points:.2f})")

    return total_score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation) tuples, highest first."""
    # Judge every song once: (song, score, reasons_list).
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # Rank by score (highest first) and keep the top k.
    top = sorted(scored, key=itemgetter(1), reverse=True)[:k]

    # Flatten each reasons list into an explanation string for the survivors.
    return [(song, score, "; ".join(reasons)) for song, score, reasons in top]
