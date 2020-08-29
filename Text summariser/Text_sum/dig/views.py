from django.shortcuts import render
#from . forms import InputForm

# Create your views here.
def index(request):
    return render (request,'page.html')

def summary(request):
    import nltk
    import re
    from nltk.stem import PorterStemmer
    # nltk.download('punkt')
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.probability import FreqDist
    from nltk.corpus import stopwords

    # s= " So, keep working. Keep striving. Never give up.Fall down seven times, get up eight.[Ease is a greater threat to progress than hardship.] So, keep moving, keep growing, keep learning. See you at work."

    article_text = request.GET['write']
    #file = open(file, 'r', encoding='utf-8')
    #article_text = file.read()
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  # removing bracket
    article_text = re.sub(r'\s+', ' ', article_text)

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    words = nltk.word_tokenize(formatted_article_text)  # tokenize
    words = [word.lower() for word in words if word.isalpha()]

    # print(words)

    stopWords = set(stopwords.words("english"))                                                    # removing english stopwords
    word = word_tokenize(formatted_article_text)
    ps = PorterStemmer()

    frequencies = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue  # frequency
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1

    sentences = sent_tokenize(article_text)

    sentValue = dict()

    for sentence in sentences:
        for word, freq in frequencies.items():
            if word in sentence.lower():
                if sentence[:10] in sentValue:
                    sentValue[sentence[:8]] += freq
                else:
                    sentValue[sentence[:8]] = freq  # average

    sum = 0
    for entry in sentValue:
        sum += sentValue[entry]

    average = int(sum / len(sentValue))

    count = 0
    summary = ''

    for sentence in sentences:
        if (sentence[:8] in sentValue) and (sentValue[sentence[:8]] > (1.5 * average)):                            # summary
            summary += " " + sentence
            count = +1
    #print(summary)
    # f1 = open("summary.txt",'w')
    # f1.write(summary)

    return render(request,'Summary.html',{'write': article_text,'summary':summary})