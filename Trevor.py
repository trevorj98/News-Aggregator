# Import modules
from newspaper import Article
import requests
from bs4 import BeautifulSoup as soup
# Welcome Message
print("Welcome to the Newspaper Aggregator Project. \n"
      "Here, you will have access to the latest articles in the technology section of the New York Times.\n")
# Use the below statement get all the html from the url and parse it
response = requests.get("https://www.nytimes.com/section/technology")
response_soup = soup(response.content, 'html.parser')
# Use the below statement as a visualizer of the HTML outline.
scripts = response_soup.find_all("script", {"type": "application/ld+json"})
#  Gets an article list - a snippet of the HTML outline including all of the articles.

articles = []
for script in scripts:
    for dictionary in script:
        articles.append(dictionary)

articles[0:2] = [''.join(articles[0:2])]
# The content string is the first element of this list.
content_string = articles[0]
# The index of the "itemListElement" is used to extract a library of all the article hyperlinks and metadata.
article_index = content_string.index("itemListElement")
# A substring of the content string is taken to remove the "itemListElement" from the string.
content_string = content_string[article_index + 18:]
# A list comprehension methodology searches for the common hyperlink beginning across all articles.
start_indices = [i for i in range(len(content_string)) if content_string.startswith('https://www.nytimes.com/2021', i)]
# A list comprehension methodology searches for the common ".html" extension at the end of each article hyperlink.
end_indices = [i for i in range(len(content_string)) if content_string.startswith('.html', i)]
# Each element of the end_indices list are incremented by 5 in order to get the last character of the hyperlink
end_indices = [x + 5 for x in end_indices]
# Validation techniques are used to equalize the lengths of the start and end indices.
if len(start_indices) > len(end_indices):
    difference = len(start_indices) - len(end_indices)
    start_indices = start_indices[:difference]

if len(end_indices) > len(start_indices):
    difference = len(end_indices) - (len(end_indices) - len(start_indices))
    end_indices = end_indices[:difference]
# Defines an empty urls list
urls = []
# Uses a for-range loop to get all the indices of start_indices list.
for i in range(len(start_indices)):
    #  Gets a substring from the content string with the starting and ending index of the hyperlink.
    #  The hyperlinks are added to the urls.
    urls.append(content_string[start_indices[i]:end_indices[i]])
# initialize a counter with 1
counter = 1
print("Read the Articles")
# Gets the article summary of the chosen URL.
for url in urls:
    print("------------------------------------------------------------------------------------------------------------")
    print("Article URL: " + str(url))
# Download article and parse it
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
# Get the authors of the article
    author_string = "Author(s): "
    for author in article.authors:
        author_string += author  # adds all authors (if more than 1) to the author string.
    print(author_string)
# Get the publish data, image url and quick summary of article
    print("Publish Date: " + str(article.publish_date.strftime("%m/%d/%Y")))
    print("Image Url: " + str(article.top_image))
    print("A Quick Article Summary\n"
          "----------------------------------------\n",
          article.summary, "\n"
                        "------------------------------------------------")
# Check if this is was the last url in the urls list
    if counter == len(urls):
        print("The articles have been successfully extracted!\n"
              "Thank you")
        break
# Ask the user if want to read next article or not
    ask = input("Enter (N/n) to read next article or Press any other to exit:   ")
    if ask in ["N","n"]:
        counter += 1
        continue
    else:
        print("The articles have been successfully read!\n"
              "Thank you")
        break
