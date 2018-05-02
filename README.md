# Text-Summarization
This repo contains code for text summarization using extractive method and flask is for working in browser.
The technique is based on extractive approach. Extractive approach means before passing data to model we extract information out of it which is relevant to us or discard otherwise.  

## Usage 
To run the project use `pip install -r requirements.txt`
Open python in terminal then 
`import nltk`
`nltk.download('punkt')`
`nltk.download('stopwords')`

## To run the project 
run `python index.py` in terminal. 

![data](https://user-images.githubusercontent.com/37182334/39509644-9ea91e94-4e04-11e8-942a-cb648d5537b3.png)
**Getting text from online new article**

![toeknize](https://user-images.githubusercontent.com/37182334/39509742-fd40f18e-4e04-11e8-8632-13ef08d63655.png)
**Tokenize the text from url**

![stopwords](https://user-images.githubusercontent.com/37182334/39509794-2583b69a-4e05-11e8-817e-630b052cdd16.png)
**Remove Stopwords**

![summarize](https://user-images.githubusercontent.com/37182334/39509856-55617410-4e05-11e8-9220-e13d87fd6a9a.png)
**Summarize text** 

