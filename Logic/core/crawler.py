from requests import get
from bs4 import BeautifulSoup
from collections import deque
from concurrent.futures import ThreadPoolExecutor, wait
from threading import Lock
import json
import re
import time

class IMDbCrawler:
    """
    put your own user agent in the headers
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }
    top_250_URL = 'https://www.imdb.com/chart/top/'
    pattern = r'^https://www\.imdb\.com/title/(tt\d{4,8})/$'
    def __init__(self, crawling_threshold=1000):
        """
        Initialize the crawler

        Parameters
        ----------
        crawling_threshold: int
            The number of pages to crawl
        """
        # TODO
        self.crawling_threshold = crawling_threshold
        self.not_crawled = []
        self.crawled = []
        self.added_ids = set()
        self.ids_lock = Lock()
        self.ncrawled_lock = Lock()
        self.crawled_lock = Lock()
        
        self.pattern = r'^https://www\.imdb\.com/title/(tt\d{4,8})/$'
        self.MAX_TRIES = 10
        self.delay = 1

    

    def get_id_from_URL(self, URL):
        """
        Get the id from the URL of the site. The id is what comes exactly after title.
        for example the id for the movie https://www.imdb.com/title/tt0111161/?ref_=chttp_t_1 is tt0111161.

        Parameters
        ----------
        URL: str
            The URL of the site
        Returns
        ----------
        str
            The id of the site
        """
        m = re.match(self.pattern, URL)
        assert m, 'Invalid URL'
        return m.group(1)
    
    def get_URL_from_id(self, id):
        return 'https://www.imdb.com/title/'+id+'/'
    
    def write_to_file_as_json(self):
        """
        Save the crawled files into json
        """
        file_path = "../IMDB_crawled.json"
        with open(file_path, "w") as json_file:
            json.dump(self.crawled, json_file, indent=4)

    def write_added_ids(self):
        with open('added_ids.json', "w") as json_file:
            json.dump(self.added_ids, json_file, indent=4)

    def read_from_file_as_json(self):
        """
        Read the crawled files from json
        """
        # TODO
        with open('IMDB_crawled.json', 'r') as f:
            self.crawled = json.load(f)

        with open('IMDB_not_crawled.json', 'r') as f:
            self.not_crawled = json.load(f)

        with open('added_ids.json', 'r') as f:
            self.added_ids = json.load(f)



    def safe_get(self, url):
        for attempt in range(1, self.MAX_TRIES + 1):
            try:
                response = get(url, headers=IMDbCrawler.headers)
                if response.status_code == 200:
                    return response
            except Exception as e:
                print(f"Seed Request failed (attempt {attempt}/{self.MAX_TRIES}): {e}")
            
            if attempt < self.MAX_TRIES:
                time.sleep(self.delay)

    def crawl(self, URL):
        """
        Make a get request to the URL and return the response

        Parameters
        ----------
        URL: str
            The URL of the site
        Returns
        ----------
        requests.models.Response
            The response of the get request
        """

        return self.safe_get(URL)



    def extract_top_250(self):
        """
        Extract the top 250 movies from the top 250 page and use them as seed for the crawler to start crawling.
        """
        # TODO update self.not_crawled and self.added_ids
        
        response = self.safe_get(IMDbCrawler.top_250_URL)
        pattern = re.compile(r'/title/(tt\d{4,8})/')

        matching_strings = pattern.findall(response.text)[::2]

        self.ids_lock.acquire()
        self.added_ids.update(matching_strings.copy())
        self.ids_lock.release()

        for i in range(len(matching_strings)):
            matching_strings[i] = self.get_URL_from_id(matching_strings[i])

        self.ncrawled_lock.acquire()
        self.not_crawled += matching_strings
        self.ncrawled_lock.release()
        
    def get_imdb_instance(self):
        return {
            'id': None,  # str
            'title': None,  # str
            'first_page_summary': None,  # str
            'release_year': None,  # str
            'mpaa': None,  # str
            'budget': None,  # str
            'gross_worldwide': None,  # str
            'rating': None,  # str
            'directors': None,  # List[str]
            'writers': None,  # List[str]
            'stars': None,  # List[str]
            'related_links': None,  # List[str]
            'genres': None,  # List[str]
            'languages': None,  # List[str]
            'countries_of_origin': None,  # List[str]
            'summaries': None,  # List[str]
            'synopsis': None,  # List[str]
            'reviews': None,  # List[List[str]]
        }

    def start_crawling(self):
        """
        Start crawling the movies until the crawling threshold is reached.
        TODO: 
            replace WHILE_LOOP_CONSTRAINTS with the proper constraints for the while loop.
            replace NEW_URL with the new URL to crawl.
            replace THERE_IS_NOTHING_TO_CRAWL with the condition to check if there is nothing to crawl.
            delete help variables.

        ThreadPoolExecutor is used to make the crawler faster by using multiple threads to crawl the pages.
        You are free to use it or not. If used, not to forget safe access to the shared resources.
        """

        # help variables
        WHILE_LOOP_CONSTRAINTS = None
        NEW_URL = None
        THERE_IS_NOTHING_TO_CRAWL = None

        self.extract_top_250()
        futures = []
        crawled_counter = 0

        with ThreadPoolExecutor(max_workers=10) as executor:
            while crawled_counter < self.crawling_threshold:

                self.ncrawled_lock.acquire()
                URL = self.not_crawled.pop(0)
                self.ncrawled_lock.release()

                futures.append(executor.submit(self.crawl_page_info, URL))
                crawled_counter += 1
                if len(self.not_crawled) == 0:
                    wait(futures)
                    futures = []

    def crawl_page_info(self, URL):
        """
        Main Logic of the crawler. It crawls the page and extracts the information of the movie.
        Use related links of a movie to crawl more movies.
        
        Parameters
        ----------
        URL: str
            The URL of the site
        """
        print("new iteration")
        #TODO
        response = self.crawl(URL)
        movie = self.get_imdb_instance()
        movie['id'] = self.get_id_from_URL(URL)
        # print(movie['id'])
        self.extract_movie_info(response, movie, URL)

        self.ncrawled_lock.acquire()
        self.ids_lock.acquire()
        for id in movie['related_links']:
            if id not in self.added_ids:
                self.not_crawled.append(self.get_URL_from_id(id))
        self.ncrawled_lock.release()
        self.ids_lock.release()

        self.crawled_lock.acquire()
        self.crawled.append(movie)
        self.crawled_lock.release()

        self.ids_lock.acquire()
        self.added_ids.update(movie['related_links'])
        self.ids_lock.release()


    def extract_movie_info(self, res, movie, URL):
        """
        Extract the information of the movie from the response and save it in the movie instance.

        Parameters
        ----------
        res: requests.models.Response
            The response of the get request
        movie: dict
            The instance of the movie
        URL: str
            The URL of the site
        """
        
        soup = BeautifulSoup(res.content, "html.parser")
        script_tag = soup.find("script", type="application/ld+json")  
        script_content = script_tag.string
        data = json.loads(script_content)
        
        plot_soup = BeautifulSoup(self.safe_get(IMDbCrawler.get_summary_link(URL)).content, "html.parser")
        review_soup = BeautifulSoup(self.safe_get(IMDbCrawler.get_review_link(URL)).content, "html.parser")            
        mpaa_soup = BeautifulSoup(self.safe_get(URL+'parentalguide').content, "html.parser")
        # print('mmmmm')

        movie['title'] = IMDbCrawler.get_title(soup)
        movie['first_page_summary'] = IMDbCrawler.get_first_page_summary(soup, data)
        # print('mtmtmtm')
        movie['release_year'] = IMDbCrawler.get_release_year(soup)
        movie['mpaa'] = IMDbCrawler.get_mpaa(mpaa_soup)
        movie['budget'] = IMDbCrawler.get_budget(soup)
        # print('mbmbmb')
        movie['gross_worldwide'] = IMDbCrawler.get_gross_worldwide(soup)
        movie['directors'] = IMDbCrawler.get_director(soup, data)
        # print('mymymymym')
        movie['writers'] = IMDbCrawler.get_writers(soup, data)
        # print('payini ride')
        movie['stars'] = IMDbCrawler.get_stars(soup, data)
        # print('m2m2m2m2')
        movie['related_links'] = IMDbCrawler.get_related_links(soup)
        movie['genres'] = IMDbCrawler.get_genres(soup, data)
        movie['languages'] = IMDbCrawler.get_languages(soup)
        movie['countries_of_origin'] = IMDbCrawler.get_countries_of_origin(soup)
        movie['rating'] = IMDbCrawler.get_rating(soup, data)
        movie['summaries'] = IMDbCrawler.get_summary(plot_soup)
        movie['synopsis'] = IMDbCrawler.get_synopsis(plot_soup)
        movie['reviews'] = IMDbCrawler.get_reviews_with_scores(review_soup)

    def get_summary_link(url):
        """
        Get the link to the summary page of the movie
        Example:
        https://www.imdb.com/title/tt0111161/ is the page
        https://www.imdb.com/title/tt0111161/plotsummary is the summary page

        Parameters
        ----------
        url: str
            The URL of the site
        Returns
        ----------
        str
            The URL of the summary page
        """
        try:
            assert re.match(IMDbCrawler.pattern, url), "URL doesn't match the pattern"
            return url + 'plotsummary'
        except:
            print("failed to get summary link")

    def get_review_link(url):
        """
        Get the link to the review page of the movie
        Example:
        https://www.imdb.com/title/tt0111161/ is the page
        https://www.imdb.com/title/tt0111161/reviews is the review page
        """

        try:
            assert re.match(IMDbCrawler.pattern, url), "URL doesn't match the pattern"
            return url + 'reviews'
        except:
            print("failed to get review link")

    def get_title(soup):
        """
        Get the title of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The title of the movie

        """
        try: 
            title_element = soup.find("h1")
            return title_element.text.strip() if title_element else "Title not found"
        except:
            print("failed to get title")
            return 'N/A'

    def get_first_page_summary(soup, data):
        """
        Get the first page summary of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The first page summary of the movie
        """
        try:
            return data.get('description')
        except:
            print("failed to get first page summary")
            return 'N/A'

    def get_director(soup, data):
        """
        Get the directors of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The directors of the movie
        """
        try:
            people = data.get('director', [])
            res = []
            for person in people:
                res.append(str(person.get('name', 'director not found')))
            return res
        
        except:
            print("failed to get director")
            return ['N/A']

    def get_stars(soup, data):
        """
        Get the stars of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The stars of the movie
        """
        try:
            people = data.get('actor', [])
            res = []
            for person in people:
                res.append(person.get('name', 'star not found'))
            return res
        except:
            print("failed to get stars")
            return ['N/A']

    def get_writers(soup, data):
        """
        Get the writers of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The writers of the movie
        """
        try:

            script_tag = soup.find('script', type='application/ld+json')

            json_data = json.loads(script_tag.string)
            writers = [writer['name'] for writer in json_data.get('creator', []) if writer.get('@type') == 'Person']
                
            return writers
        except:
            print("failed to get writers")
            return ['N/A']

    def get_related_links(soup):
        """
        Get the related links of the movie from the More like this section of the page from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The related links of the movie
        """
        try:
            res = []
            poster_divs = soup.find_all('div', class_='ipc-poster ipc-poster--base ipc-poster--dynamic-width ipc-poster-card__poster ipc-sub-grid-item ipc-sub-grid-item--span-2')
            for div in poster_divs:
                link = div.find('a', class_='ipc-lockup-overlay')
                href_value = link.get('href')   
                pattern = re.compile(r'/title/(tt\d{6,8})/')
                matching_strings = pattern.search(href_value)
                res.append(matching_strings.group()[7:-1])
            return res
        except:
            print("failed to get related links")
            return ['N/A']

    def get_summary(soup):
        """
        Get the summary of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The summary of the movie
        """
        try:
            summary_section = soup.find('section', class_='ipc-page-section--base')
            summaries = []
            summary_items = summary_section.find_all('li', class_='ipc-metadata-list__item')

            for item in summary_items:
                summary_div = item.find('div', class_='ipc-html-content-inner-div')

                if summary_div:
                    summary_text = summary_div.get_text(strip=True)
                    summaries.append(summary_text)

            return summaries[1:]
        except:
            print("failed to get summary")
            return ['N/A']

    def get_synopsis(soup):
        """
        Get the synopsis of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The synopsis of the movie
        """
        try:
            synopsis_div = soup.select_one('div[data-testid="sub-section-synopsis"]')
            synopsis = ""
            ul_tag = synopsis_div.find('ul', class_='ipc-metadata-list')
            li_tag = ul_tag.find('li', class_='ipc-metadata-list__item')
            synopsis = li_tag.get_text(strip=True)

            return [synopsis]
        except:
            print("failed to get synopsis")
            return ['N/A']

    def get_reviews_with_scores(soup):
        """
        Get the reviews of the movie from the soup
        reviews structure: [[review,score]]

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[List[str]]
            The reviews of the movie
        """
        try:
            res = []
            lister_list_div = soup.find('div', class_='lister-list')
            reviews = lister_list_div.find_all('div', class_='review-container')
            
            for review in reviews:
                rating_span = review.find('span', class_='rating-other-user-rating')
                if rating_span:
                    rating = rating_span.get_text(strip=True)
                else:
                    rating = "N/A" 
                
                review_text_div = review.find('div', class_='text show-more__control')
                if review_text_div:
                    review_text = review_text_div.get_text(separator='\n', strip=True)
                else:
                    review_text = "N/A"
                
                res.append((review_text, str(rating)))
            return res
        except:
            print("failed to get reviews")
            return [['N/A', 'N/A']]

    def get_genres(soup, data):
        """
        Get the genres of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The genres of the movie
        """
        try:
            genres = data.get('genre', [])
            return genres
        except:
            print("Failed to get generes")
            return ['N/A']

    def get_rating(soup, data):
        """
        Get the rating of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The rating of the movie
        """
        try:
            rating = data.get('aggregateRating', {}).get('ratingValue')
            return str(rating)
        except:
            print("failed to get rating")
            return 'N/A'

    def get_mpaa(soup):
        """
        Get the MPAA of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The MPAA of the movie
        """
        try:
            mpaa_element = soup.find('tr', id='mpaa-rating')
            mpaa_rating = mpaa_element.find_all('td')[1].get_text(strip=True)

            return mpaa_rating
        except:
            print("failed to get mpaa")
            return 'N/A'

    def get_release_year(soup):
        """
        Get the release year of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The release year of the movie
        """
        try:
            script_tag = soup.find("script", type="application/json")  
            script_content = script_tag.string
            data = json.loads(script_content)
            return str(data['props']['pageProps']['aboveTheFoldData']['releaseYear']['year'])
        except:
            print("failed to get release year")
            return 'N/A'

    def get_languages(soup):
        """
        Get the languages of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The languages of the movie
        """
        try:
            languages_li = soup.find('li', attrs={"data-testid": "title-details-languages"})
            language_links = languages_li.find_all('a', class_='ipc-metadata-list-item__list-content-item--link')
            languages = [link.get_text(strip=True) for link in language_links]
            return languages
        except:
            print("failed to get languages")
            return ['N/A']

    def get_countries_of_origin(soup):
        """
        Get the countries of origin of the movie from the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        List[str]
            The countries of origin of the movie
        """
        try:
            countries_section = soup.find('li', {'data-testid': 'title-details-origin'})
            
            country_links = countries_section.find_all('a', class_='ipc-metadata-list-item__list-content-item')
            countries = [link.text.strip() for link in country_links]
            return countries
        except:
            print("failed to get countries of origin")
            return ['N/A']

    def get_budget(soup):
        """
        Get the budget of the movie from box office section of the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The budget of the movie
        """
        try:
            budget_element = soup.find(attrs={"data-testid": "title-boxoffice-budget"})
            desired_element = budget_element.find(class_="ipc-metadata-list-item__list-content-item")
            return desired_element.text.strip()
        except:
            print("failed to get budget")
            return 'N/A'

    def get_gross_worldwide(soup):
        """
        Get the gross worldwide of the movie from box office section of the soup

        Parameters
        ----------
        soup: BeautifulSoup
            The soup of the page
        Returns
        ----------
        str
            The gross worldwide of the movie
        """
        try:
            budget_element = soup.find(attrs={"data-testid": "title-boxoffice-cumulativeworldwidegross"})
            desired_element = budget_element.find(class_="ipc-metadata-list-item__list-content-item")
            return desired_element.text.strip()
        except:
            print("failed to get gross worldwide")
            return 'N/A'


def main():
    imdb_crawler = IMDbCrawler(crawling_threshold=1005)
    # imdb_crawler.read_from_file_as_json()
    imdb_crawler.start_crawling()
    imdb_crawler.write_to_file_as_json()


if __name__ == '__main__':
    main()


