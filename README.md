This is my University project on Music Recommendation using neural networks

### Status:
(kind of) Trained the model for text comparison (it still needs some work).
Trying to train a model for audio comparison...

### Data:
1. [Last.fm dataset](http://labrosa.ee.columbia.edu/millionsong/lastfm), the official song tags and song similarity collection for the Million Song Dataset.
2. Audio samples from Deezer ([API](http://developers.deezer.com/)).
3. Lyrics from Genius ([API](https://genius.com/developers)).

### Dependencies
- Python (tested with 3.5.2)
- Theano + Keras
- [librosa](https://github.com/librosa/librosa) (a python package for music and audio analysis)
- (__optional__) [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (you don't need this if you won't use parselyrics.py to get lyrics from html pages)

### Known Issues
- DatasetBuilder eats all the memory (need to fix this)
