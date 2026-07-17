# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.


Real-world recommendation engines like Spotify’s BaRT predict preferences by blending user behavior with track metadata. While streaming giants use massive architectures, they remain vulnerable to the "cold-start problem" for new songs with zero listening history. To bypass this, I implemented a content-based filtering approach in my simulation that maps track attributes directly to a user's explicit profile.

* **Song Features:** Each song in my system uses categorical strings (`genre`, `mood`) and normalized decimal values (`energy`, `tempo_bpm`, `valence`, `danceability`).

* **UserProfile Information:** I store the user's target preferences for those exact same attributes (`preferred_genre`, `preferred_mood`, `target_energy`, etc.).

* **Score Computation:** My `Recommender` computes a score by calculating the absolute mathematical distance between the user’s target values and a song's attributes, subtracting that distance from 1 so closer matches get higher scores.

* **Recommendation Choice:** I apply weights to favor crucial features (like genre over tempo), sort the entire catalog by their final combined scores, and recommend the top-ranked tracks.


### My Taste Profile Dictionary

I am using this specific profile configuration to test my comparisons:

```python
user_profile = {
    "preferred_genre": "synthwave",
    "preferred_mood": "focused",
    "target_energy": 0.75,
    "target_tempo": 0.65,        # Scaled 0.0 - 1.0 equivalent of ~115 BPM
    "target_valence": 0.50,      # Emotionally neutral / atmospheric
    "target_danceability": 0.60  # Moderately rhythmic but not distracting
}

My program uses a multi-step mathematical approach to score each song by evaluating its categorical and numerical distance from the user's taste profile.

1. Categorical Filtering (Exact Match)For text-based features, the rule is binary. 

If a song matches the exact string, it receives a full score for that category; otherwise, it receives zero.Genre Score: If song["genre"] == user_profile["preferred_genre"], the score is 1.0, else 0.0.

Mood Score: If song["mood"] == user_profile["preferred_mood"], the score is 1.0, else 0.0.

2. Numerical Proximity (Absolute Distance)For continuous values, the algorithm calculates how close a song's feature is to the user's target value. To reward closeness rather than simply higher or lower values, I calculate the Absolute Difference and subtract it from 1.0.

Feature Score = 1.0 - |u_target - s_actual|

This logic applies to energy, tempo_bpm, valence, and danceability.

3. Feature Weighting & Ranking (The Final Blend)To give certain features more influence over the recommendations, I multiply each individual score by a pre-defined weight parameter:

Total Score = (2.0 x Genre Score) + (2.0 x Mood Score) + (1.0 x Energy Score) + (1.0 x Tempo Score) + (0.5 x Valence Score) + (0.5 x Danceability Score)

Once every song in the catalog has its Total Score calculated, the ranking rule sorts the collection in descending order and selects the top tracks.

Potential Biases & Limitations
Because I heavily weighted the categorical matches (setting Genre and Mood multiplier to 2.0), the system naturally creates a bit of an echo chamber. It tends to hyper-focus on exact genre matches, meaning it might completely ignore an incredible rock or ambient track that perfectly nails the user's desired mood, energy, and tempo. Furthermore, since it's entirely content-based, it can't make those unexpected, cross-genre leaps that make you say, "How did it know I'd like this?"—a magic touch that only collaborative filtering can provide by looking at real human behavior.



---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

Top 5 picks for a "synthwave / focused" profile
===============================================

#1  Night Drive Loop (Neon Echo)   score: 4.88
      - genre match (+2.0)
      - energy match (+1.00)
      - tempo match (+0.95)
      - valence match (+0.49)
      - danceability match (+0.43)

#2  Focus Flow (LoRoom)   score: 4.25
      - mood match (+2.0)
      - energy match (+0.65)
      - tempo match (+0.65)
      - valence match (+0.46)
      - danceability match (+0.50)

#3  Rooftop Lights (Indigo Parade)   score: 2.64
      - energy match (+0.99)
      - tempo match (+0.91)
      - valence match (+0.34)
      - danceability match (+0.39)

#4  Sunrise City (Neon Echo)   score: 2.63
      - energy match (+0.93)
      - tempo match (+0.97)
      - valence match (+0.33)
      - danceability match (+0.40)

#5  Concrete Kings (Rhyme Foundry)   score: 2.60
      - energy match (+0.97)
      - tempo match (+0.81)
      - valence match (+0.44)
      - danceability match (+0.38)

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

* **Lowering the Genre Weight:** I changed the genre weight from 2.0 down to 0.5. This stopped the system from hyper-focusing on exact genre matches. As a result, more diverse styles of music started showing up in the top recommendations.

* **Adding Tempo and Valence:** Adding these numbers allowed the system to separate fast, happy songs from slow, sad ones. It made the recommendations feel much more specific to the user's current mood.

* **Testing Different Users:** The system worked great for extreme profiles like a workout fan or a quiet study session. However, it struggled with casual users who wanted a mix of different genres at the same time.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

* **Tiny Catalog:** The system only works on a tiny database of songs[cite: 1]. This forces the algorithm to repeat the same tracks too often.

* **No Lyric Tracking:** The code does not understand lyrics, language, or song meaning. It only looks at raw numbers and basic category tags.

* **Echo Chambers:** The scoring system heavily favors exact genre and mood matches. This can lock a user into a repetitive loop where they never discover new types of music.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Building this project showed me how much data shapes a recommendation engine. I learned that rigid weights can easily lock a user into a boring echo chamber. It completely changed how I view my own music apps because now I see the mathematical trade-offs happening behind my playlists.

My biggest learning moment was discovering how heavily a dataset's size impacts the accuracy of the recommendations. Even when my formulas worked perfectly, the small pool of songs forced the algorithm to make odd trade-offs. Using AI tools helped me write the base code quickly, but I had to double-check how it accessed python dataclasses versus standard dictionaries. I was surprised that basic addition and subtraction could still make the system "feel" like it was reading my mind. If I extended this project, I would add an automatic fallback feature to suggest songs from adjacent genres when an exact match is missing.