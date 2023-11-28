import scrapy
from pathlib import Path
import logging
from bs4 import BeautifulSoup as bs

logging.basicConfig(filename="logger.log", level=logging.INFO, format='%(asctime)s (%(lineno)d) ---  %(message)s')

class FlipkartSpider(scrapy.Spider):
    logging.info("Scraping Started!")
    name = "flipkart_"

    def __init__(self, url='', **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [url]


    def parse(self, response):
        logging.info("Search page scraping started!")
        global product_url
        body = response.body
        body_html = bs(body, 'html.parser')

        try:
            page_div = body_html.findAll("div", {"class":"_1AtVbE col-12-12"})
            logging.info(f"page div value: {page_div}")
        except Exception as e:
            logging.info(e)
        
        product_url = "https://www.flipkart.com" + page_div[3].div.div.div.a['href']
        logging.info("product url: ",product_url)

        yield response.follow(product_url, callback=self.parse_page)

    def parse_page(self, response):
        logging.info("Product page scraping started!")
        body = response.body
        body_html = bs(body, 'html.parser')
        
        try:
            commentboxes = body_html.find_all("div", {"class":"_16PBlm"})
            logging.info(f"len of commentboxes {len(commentboxes)}")
            logging.info(commentboxes)
        except Exception as e:
            logging.info(e)

        try :
            product = body_html.find("div", {"class": "aMaAEs"})
        except Exception as e:
            logging.info(e)
        try:
            product_name = product.find_all("span", {"class":"B_NuCI"})[0].text
            logging.info(f"product name: {product_name}")
        except:
            logging.info("no product name")
        review_list = []
        for comment in commentboxes:
            try:
                name = comment.find("p", {"class":"_2sc7ZR _2V5EHH"}).text
                logging.info(f"name: {name}")
            except :
                name = 'no name'
                logging.info("name is empty")
            
            try:
                rating = rating = comment.div.div.div.div.text
                logging.info(f"rating: {rating}")
            except:
                rating = 'no rating'
                logging.info("no rating found!")

            try:
                comment_heading = comment.div.div.div.p.text
                logging.info(f"comment heading: {comment_heading}")
            except:
                comment_heading = 'no comment heading'
                logging.info("No comment heading found!")
            
            try:
                review_tag = comment.div.div.find_all("div", {"class":""})
                review = review_tag[0].div.text
                logging.info(f"review: {review}")
            except Exception as e:
                logging.info(e)
            
            my_dict = {"Product": product_name,"Name": name, "Rating": rating, "CommentHead": comment_heading, "Comment": review,"URL": product_url}
            
            review_list.append(my_dict)

            yield my_dict