import streamlit as st
from google_play_scraper import Sort, reviews_all, reviews
from urllib.parse import urlparse, parse_qs
from streamlit_download import download_button
import pandas as pd
import base64

class ReviewScraper:
    def __init__(self, url, count, filter_score):
        self.url = url
        self.count = count
        self.filter_score = filter_score

    def get_app_id(self):
        parsed_url = urlparse(self.url)
        if 'play.google.com' in parsed_url.netloc:
            parameters = parse_qs(parsed_url.query)
            return parameters.get('id', [None])[0]
        return None

    def scrape_reviews(_self):
        app_id = _self.get_app_id()
        
        if app_id:
            result, continuation_token = reviews(
                app_id,
                sort=Sort.NEWEST,
                count=_self.count, 
                filter_score_with=_self.filter_score
            )
            return result
        else:
            return None

    def scrape_all_reviews(self):
        st.write("Fetching all reviews from playstore. Please wait.. ")
        app_id = self.get_app_id()
        
        if app_id:
            result = reviews_all(
                app_id,
                sort=Sort.NEWEST,
                filter_score_with=self.filter_score
            )
            return result
        else:
            return None

st.set_page_config(page_title="Playstore Scraper",page_icon = "logo.png" )
st.title('Google Play Store Reviews Scraper')

# Inputs
st.write("""
Enter the Google Play Store URL below and press 'Scrape Reviews' to begin.
""")
url = st.text_input('Google Play Store URL:')

fetch_option = st.selectbox('Choose review fetch option:', options=["All", "Some"])
if fetch_option == "Some":
    all_reviews = False
    count = st.number_input('Number of reviews to scrape:', min_value=1, max_value=None, value=50)
else:
    all_reviews = True
    count = None
filter_score = st.selectbox('Filter by Rating:', options=[None, 1, 2, 3, 4, 5])


# Button to start scraping
if st.button('Scrape Reviews'):
    # Initialize the ReviewScraper class
    scraper = ReviewScraper(url, count, filter_score)
    
    # Scrape the reviews
    if all_reviews:
        reviews = scraper.scrape_all_reviews()
    else:
        reviews = scraper.scrape_reviews()
    
    # Check if reviews were found
    if reviews:
        reviews_df = pd.DataFrame(reviews)
        positive_review_button = download_button(reviews_df,'playstore_reviews.csv','Click to download Reviews')
        st.markdown(positive_review_button, unsafe_allow_html=True)
    else:
        st.write("Invalid Google Play Store URL. Please check the URL and try again.")
