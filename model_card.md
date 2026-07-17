# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**MusicSuggestor**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This model is designed for classroom exploration to show how basic recommendation systems work. It generates a top tracks list for a user by analyzing a static spreadsheet of songs. It assumes the user knows exactly what kind of musical style, mood, and sound settings they want to hear. It is not meant for real, commercial deployment.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The model looks at several properties for every single song in the database. It checks text categories like genre and mood, alongside number ratings like energy, tempo, valence, and danceability. It evaluates the user's specific target settings and finds the mathematical difference for each trait. Closer numbers get higher scores, while exact text matches get a large bonus point boost. The model then adds up these scores using custom weights, sorts the list from highest to lowest, and hands the user the best options.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The simulator runs on a tiny dataset of just 10 individual songs. The catalog features a handful of distinct genres like pop, lofi, rock, synthwave, ambient, and jazz. No extra songs were added or removed from the base starter file. Because the dataset is so small, huge parts of musical taste are missing, including full albums, actual vocals, and cultural trends.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works great for users who have a very clear, rigid idea of what they want to listen to. It does a solid job capturing extreme vibe differences, like separating a fast workout track from a sleepy study beat. The text matching rules ensure that if a song perfectly fits your favorite genre, it will almost always rise to the top of your list.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

This system has a major blind spot because the dataset is too small. With only ten songs, it forces the computer to recommend the same tracks repeatedly. If you pick a rare genre, you will get stuck in a tiny loop of one or two options. The code also completely ignores vocals, lyrics, and artist names. This means it might mistake an instrumental study track for a loud rock song just because their speed numbers match.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

To check the math, I tested the system with three different profiles: "Study Session," "Gym Hero," and "Sunny Day." I watched to see if changing the preferences actually shifted the track list. 

I was surprised by how easily a heavy gym track could sneak into a happy pop playlist. This happens because the dataset is tiny, so the algorithm has to compromise. If it runs out of pop songs, it picks the gym song because both share high energy numbers.

* **"Gym Hero" vs. "Study Session":** Switching profiles completely flipped the results from fast synthwave to slow lofi beats. The absolute distance formula correctly penalized high energy when looking for calm tracks.
    
* **"Gym Hero" vs. "Sunny Day":** The gym track appeared at the bottom of the pop playlist because both profiles look for high energy and danceability. The math decided the gym song was close enough, even though the genres did not match.

* **"Sunny Day" vs. "Study Session":** The pop profile wanted happy tracks, while the study profile wanted neutral tracks. Because of this, the bright pop tracks disappeared entirely when switching to the study settings.


---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I want to add a filter to stop the same artist from clogging the top results. I would also scale up the database to include thousands of tracks so the formula has better options. Finally, I want to add a rule that injects random surprise genres to keep things interesting.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this project showed me how much data shapes a recommendation engine. I learned that rigid weights can easily lock a user into a boring echo chamber. It completely changed how I view my own music apps because now I see the mathematical trade-offs happening behind my playlists.

My biggest learning moment was discovering how heavily a dataset's size impacts the accuracy of the recommendations. Even when my formulas worked perfectly, the small pool of songs forced the algorithm to make odd trade-offs. Using AI tools helped me write the base code quickly, but I had to double-check how it accessed python dataclasses versus standard dictionaries. I was surprised that basic addition and subtraction could still make the system "feel" like it was reading my mind. If I extended this project, I would add an automatic fallback feature to suggest songs from adjacent genres when an exact match is missing.