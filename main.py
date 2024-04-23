import streamlit as st
from google_play_scraper import Sort, reviews_all, reviews
import google_play_scraper as gps
from urllib.parse import urlparse, parse_qs
from streamlit_download import download_button
import pandas as pd
import base64
import re
from app_store_scraper import AppStore
from appstore_fetcher import *


class ReviewScraper:
    def __init__(self, url, count, filter_score):
        self.url = url
        self.count = count
        self.filter_score = filter_score
        self.playstore_app_id = None

    def get_app_id(self):
        parsed_url = urlparse(self.url)
        if 'play.google.com' in parsed_url.netloc:
            parameters = parse_qs(parsed_url.query)
            app_id = parameters.get('id', [None])[0]
            self.playstore_app_id = app_id
            return app_id
        return None
    
    def get_playstore_app_name(self):
        app_details = gps.app(self.playstore_app_id)
        playstore_app_name = app_details['title']
        return playstore_app_name

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
    

if __name__ == "__main__":

    st.set_page_config(page_title="Review Scraper",page_icon = "logo.png" )
    st.title('Play Store & App Store Reviews Scraper')

    fetch_option = st.selectbox('Choose the platform to fetch reviews from:', options=["Google Playstore","Apple Appstore"])

    if fetch_option == 'Apple Appstore':

        
        st.write("""
        Enter the App Store URL below and press 'Scrape Reviews' to begin.
        """)    
        url = st.text_input('App Store URL:')
        my_app_name_ = get_app_name_from_link(url)
        my_app_id_ = get_id_from_link(url)

        if st.button('Scrape Reviews'):
            try:
                review_fetcher = AppStore(country="in", app_name = my_app_name_, app_id = my_app_id_)
                review_fetcher.review()
                reviews_df = pd.DataFrame(review_fetcher.reviews)
                reviews_df.sort_values(by = 'date',ascending= False,inplace = True)
                
                positive_review_button = download_button(reviews_df,f'{my_app_name_}_appstore_reviews.csv','Click to download Reviews')
                st.markdown(positive_review_button, unsafe_allow_html=True)
            except:
                st.write("Invalid App Store URL. Please check the URL and try again.")


    elif fetch_option == 'Google Playstore':

        st.write("""
        Enter the Google Play Store URL below and press 'Scrape Reviews' to begin.
        """)
        url = st.text_input('Google Play Store URL:')

        all_reviews = True
        count = None
        filter_score = None
        # filter_score = st.selectbox('Filter by Rating:', options=[None, 1, 2, 3, 4, 5])


        if st.button('Scrape Reviews'):
            scraper = ReviewScraper(url, count, filter_score)
            
            if all_reviews:
                reviews = scraper.scrape_all_reviews()
            else:
                reviews = scraper.scrape_reviews()
            
            if reviews:
                reviews_df = pd.DataFrame(reviews)
                reviews_df.sort_values(by = 'at',ascending=False,inplace=True)

                playstore_app_name = scraper.get_playstore_app_name()
                positive_review_button = download_button(reviews_df,f'{playstore_app_name}_playstore_reviews.csv','Click to download Reviews')
                st.markdown(positive_review_button, unsafe_allow_html=True)
            else:
                st.write("Invalid Google Play Store URL. Please check the URL and try again.")


                
