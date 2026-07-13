from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
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


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dicts, converting the numeric
    columns to floats. Missing/blank numeric fields become None.
    Required by src/main.py
    """
    numeric_fields = {
        "energy", "tempo_bpm", "valence", "danceability",
        "acousticness", "instrumentalness", "speechiness",
    }
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in numeric_fields:
                value = row.get(field)
                if value is None or value == "":
                    row[field] = None
                else:
                    row[field] = float(value)
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song (dict) against user preferences (dict).
    user_prefs keys: "genre", "mood", "energy".
    Returns (score, reasons).
    """
    return _score(
        user_prefs.get("genre", ""),
        user_prefs.get("mood", ""),
        float(user_prefs.get("energy", 0.0)),
        song.get("genre", ""),
        song.get("mood", ""),
        float(song.get("energy") or 0.0),
    )


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, sorts by score descending, and returns the top k as
    (song_dict, score, explanation) tuples.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
