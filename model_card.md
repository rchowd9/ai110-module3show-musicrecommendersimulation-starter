# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

While my recommender works well for direct matches, it has a major blind spot when it comes to variety because of how the dataset is built. With such a tiny catalog, certain genres and moods are heavily underrepresented, which forces the algorithm to overfit to the few options it has. For example, because the system heavily weights exact category matches, a user who prefers a rare genre might get stuck in a repetitive loop of the same one or two songs, even if other tracks in the database fit their exact numerical vibe. Additionally, the scoring logic completely ignores critical musical elements like artist variety, vocals, and lyrics, meaning it can't distinguish between an instrumental study track and a vocal-heavy song as long as their raw energy and tempo values are similar.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

To make sure the scoring math was actually doing its job, I tested the recommender using three distinct user profiles designed to represent very different listening vibes:

* **The "Study Session" (Lofi/Focused):** Prefers low-energy, relaxed, and focused instrumental music.
* **The "Gym Hero" (Synthwave/Intense):** Prefers high-energy, fast-tempo, and intense tracks to workout to.
* **The "Sunny Day" (Happy Pop):** Prefers high-valence (very happy), high-danceability, medium-energy tracks.

### What I Looked For & What Surprised Me
I wanted to make sure that changing a preference actually shifted the recommendations in a logical way, rather than the algorithm just spitting out the same popular songs over and over. 

What surprised me most was how easily a high-energy song (like a gym track) could "steer" its way into a playlist meant for a totally different vibe (like happy pop). In a tiny dataset, if there aren't enough perfect matches, the mathematical "distance" calculation has to compromise. It realizes, "Well, I don't have any happy pop songs left, but this gym track has the exact high energy and high danceability you asked for!" To a human, a heavy synthwave gym track feels completely out of place on a sunny pop playlist, but to the computer, the numbers matched up almost perfectly.

### Profile Comparisons (How the Output Shifted)

To prove the algorithm's math makes sense, here is how the outputs shifted when comparing the profiles:

* **"Gym Hero" vs. "Study Session":** When switching from the Gym profile to the Study profile, the recommendations completely flipped from high-tempo, driving synthwave tracks to slow, ambient, and lofi beats. This makes perfect sense because the absolute distance formula penalized high-energy values, forcing the system to surface tracks with low energy ratings and calm moods.
    
* **"Gym Hero" vs. "Sunny Day" (Why the Gym song shows up for Happy Pop):** Even though these feel like different vibes, the "Gym Hero" track kept showing up at the bottom of the "Sunny Day" pop recommendations. This happened because both profiles share high target values for energy and danceability. Because my code treats these numerical values as a major part of the score, the math decided the gym song was a "close enough" fit for a happy pop listener, even if the genre didn't match.

* **"Sunny Day" vs. "Study Session":** The "Sunny Day" profile heavily favored tracks with high valence (emotional positivity), whereas the "Study Session" profile preferred neutral or lower valence (atmospheric/focused). As a result, the cheerful, high-tempo pop tracks disappeared entirely when switching to the study profile, replaced by quiet, emotionally flat ambient tracks that won't distract you while working.



---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
