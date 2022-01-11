# activating the package
library(stylo)

# setting a working directory that contains the corpus, e.g.
setwd("/home/henry/Documents/Code/Faffing (Totally useless)/A_Small_Collection_Of_Books")

# loading the files from a specified directory:
tokenized.texts = load.corpus.and.parse(files = "all")

# computing a list of most frequent words (trimmed to top 2000 items):
features = make.frequency.list(tokenized.texts, head = 2000)

# producing a table of relative frequencies:
data = make.table.of.frequencies(tokenized.texts, features, relative = TRUE)

print(data)

# who wrote "Pride and Prejudice"? (in my case, this is the 4th row in the table):
imposters(reference.set = data[-c(3),], test = data[1,])