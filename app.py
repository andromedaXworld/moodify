from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from textblob import TextBlob


app = Flask(__name__)

#client ID and secret client ID from spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="afe665d721fe4d10b82bb36852876c3e", client_secret="64becd6dec3041779fd9b15a51be8419"))

def analyze_mood(mood_input): #for mood analysis
    analysis = TextBlob(mood_input)
    return analysis.sentiment.polarity

def recommend_songs(mood): #for song recommendations based on entered moods
    if mood > 0.7: 
        query = "joyous upbeat pop"  
    elif 0.4 < mood <= 0.7:  
        query = "motivational rock"  
    elif 0.1 < mood <= 0.4:  
        query = "happy indie"  
    elif -0.1 < mood <= 0.1:  
        query = "chill acoustic"  
    elif -0.4 < mood <= -0.1:  
        query = "sad country"  
    elif -0.7 < mood <= -0.4:  
        query = "heartbreaking ballad"  
    else: 
        query = "emotional orchestral" 

    results = sp.search(q=query, type='track', limit=5)
    recommendations = []

    if results['tracks']['items']:  
        for track in results['tracks']['items']:
            album_image_url = track['album']['images'][0]['url']
            recommendations.append({ #displaying the song name, artist name, spotify link and the album cover for each recommendation
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'spotify_link': track['external_urls']['spotify'],
                'album_image_url': album_image_url
            })
    else:
        recommendations.append({'title': 'No song found', 'artist': '', 'spotify_link': '', 'album_image_url': ''}) #if mood isn't valid or understood no song is returned 

    return recommendations

        

@app.route('/') #Flask routing 
def index():
    return render_template('index.html') #connecting the HTML file "index.html"

@app.route('/submit', methods=['POST'])
def submit():  #for displaying recommendations 
    user_inp = request.form['mood'] 
    mood_score = analyze_mood(user_inp)  
    recommendations = recommend_songs(mood_score)  

    return render_template('index.html', recommendations=recommendations)

if __name__ == "__main__": #debugging 
    app.run(debug=True)










