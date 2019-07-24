import sqlite3 as sql
#import pandas as pd
import os
#from urllib.request import urlopen as url
#from bs4 import BeautifulSoup as bs


# CHECK WORKING DIRECTORY
os.getcwd()


# TSV TO DATAFRAME
# df = pd.read_csv('Combine.tsv', sep = '\t', error_bad_lines = False)


# CREATE DATABASE
conn = sql.connect('amazon.db')
cur = conn.cursor()


# DATAFRAME TO DATABASE
# df.to_sql('fulldata', conn, if_exists = 'replace', index = False)
# conn.commit()


# ELIMINATE SOME BAD ROWS
# cur.execute('DELETE FROM fulldata '
#             'WHERE product_category NOT IN ( '
#                 '"Health & Personal Care", "Beauty", "Apparel", "Shoes", '
#                 '"Camera", "Outdoors", "Jewelry", "Watches", "Luggage", '
#                 '"Sports");')
# conn.commit()


# REMOVE UNUSEFUL ROWS (HAVING A HELPFUL VOTE RATE < 0.9)
# cur.execute('DELETE FROM fulldata '
#             'WHERE total_votes = 0 OR (helpful_votes / total_votes) < 0.9;')
# conn.commit()


# TABLE FOR PRODUCTS
# cur.execute('DROP TABLE products;')
# cur.execute('CREATE TABLE products( '
#                 'product_id TEXT PRIMARY KEY, '
#                 'marketplace TEXT, '
#                 'product_parent TEXT, '
#                 'product_title TEXT, '
#                 'product_category TEXT, '
#                 'review_concat TEXT, '
#                 'color TEXT, '
#                 'adjective TEXT);')
# cur.execute('INSERT INTO products('
#                 'product_id, marketplace, product_parent, product_title, '
#                 'product_category, review_concat) '
#             'SELECT product_id, marketplace, product_parent, product_title, '
#                 'product_category, '
#                 'GROUP_CONCAT(review_headline || " " || review_body, " ") '
#                 'AS review_concat '
#             'FROM fulldata '
#             'GROUP BY product_id;')
# conn.commit()


# TABLE FOR REVIEWS
# cur.execute('DROP TABLE reviews;')
# cur.execute('CREATE TABLE reviews( '
#                 'review_id TEXT PRIMARY KEY, '
#                 'product_id TEXT, '
#                 'customer_id TEXT, '
#                 'star_rating TEXT, '
#                 'helpful_votes INT, '
#                 'total_votes INT, '
#                 'review_headline TEXT, '
#                 'review_body TEXT, '
#                 'color TEXT, '
#                 'adjective TEXT);')
# cur.execute('INSERT INTO reviews('
#                 'review_id, product_id, customer_id, star_rating, '
#                 'helpful_votes, total_votes, review_headline, review_body) '
#             'SELECT review_id, product_id, customer_id, star_rating, '
#                 'helpful_votes, total_votes, review_headline, review_body '
#             'FROM fulldata;')
# conn.commit()


# CHECK RESULTS
cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
print(cur.fetchall()) # tables
cur.execute('PRAGMA table_info(products);')
print(cur.fetchall()) # fields


cur.execute('SELECT COUNT(1) FROM fulldata;')
print(cur.fetchall()) # 32,656,894 rows (7,032,979 AFTER REMOVAL)

cur.execute('SELECT COUNT(DISTINCT product_id) FROM fulldata;')
print(cur.fetchall()) # 7,657,738 unique products
cur.execute('SELECT COUNT(DISTINCT review_id) FROM fulldata;')
print(cur.fetchall()) # 32,656,894 unique reviews (no duplicates in review_id)
cur.execute('SELECT COUNT(DISTINCT product_category) FROM fulldata;')
print(cur.fetchall()) # 10 unique product categories

cur.execute('SELECT AVG(LENGTH(review_headline)) FROM fulldata;')
print(cur.fetchall()) # Average length of review headline is 22.13
cur.execute('SELECT LENGTH(review_headline) '
            'FROM fulldata '
            'ORDER BY LENGTH(review_headline) '
            'LIMIT 1 '
            'OFFSET (SELECT COUNT(1) FROM fulldata) / 2;')
print(cur.fetchall()) # Median length of review headline is 15

cur.execute('SELECT AVG(LENGTH(review_body)) FROM fulldata;')
print(cur.fetchall()) # Average length of review body is 246.34
cur.execute('SELECT LENGTH(review_body) '
            'FROM fulldata '
            'ORDER BY LENGTH(review_body) '
            'LIMIT 1 '
            'OFFSET (SELECT COUNT(1) FROM fulldata) / 2;')
print(cur.fetchall()) # Median length of review body is 144

cur.execute('SELECT COUNT(1) FROM fulldata WHERE total_votes > 0;')
print(cur.fetchall()) # 12,638,361 reviews have at least one vote
cur.execute('SELECT COUNT(1) FROM fulldata '
            'WHERE total_votes > 0 AND (helpful_votes / total_votes) > 0.1;')
print(cur.fetchall()) # 10,403,247 reviews have a helpful vote rate > 0.1
cur.execute('SELECT COUNT(1) FROM fulldata '
            'WHERE total_votes > 0 AND (helpful_votes / total_votes) > 0.5;')
print(cur.fetchall()) # 8,891,095 reviews have a helpful vote rate > 0.5
cur.execute('SELECT COUNT(1) FROM fulldata '
            'WHERE total_votes > 0 AND (helpful_votes / total_votes) > 0.9;')
print(cur.fetchall()) # 6,993,780 reviews have a helpful vote rate > 0.9

cur.execute('SELECT COUNT(DISTINCT product_id) FROM fulldata '
            'WHERE helpful_votes > 1;')
print(cur.fetchall()) # 1,871,104 products have at least one helpful vote

cur.execute('SELECT AVG(LENGTH(review_body)) FROM fulldata;')


# DISCONNECT
# conn.execute("VACUUM")
cur.close();
conn.close();

# COLOR LIST
#html = url('http://www.w3schools.com/colors/colors_names.asp').read()
#soup = bs(html, 'html.parser')
#children = [item.findChildren() for item in soup.find_all('tr')]
#colors = [''.join(' ' + x if 'A' <= x <= 'Z'
#                  else x for x in item[0].text.replace(u'\xa0', '')
#                  ).strip().lower() for item in children]
#print(colors)


# COLUMN NAME
#cur.execute('PRAGMA table_info(fulldata);')
#res = cur.fetchall()
#for x in res:
#    print(x[1])
#marketplace - products
#customer_id - reviews INT
#review_id
#product_id - products, reviews
#product_parent - products INT
#product_title - products
#product_category - products
#star_rating - reviews
#helpful_votes
#total_votes
#vine
#verified_purchase
#review_headline
#review_body - reviews
#review_date