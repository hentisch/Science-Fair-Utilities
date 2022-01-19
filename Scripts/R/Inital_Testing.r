#code largely divided from https://computationalstylistics.github.io/docs/imposters

# activating the package
library(stylo)
library(dplyr)

# setting a working directory that contains the corpus, e.g.
setwd("/home/henry/Documents/Code/Open_Source/Science-Fair-Utilities/Scripts/R/Downloader")

# loading the files from a specified directory:
tokenized.texts <- load.corpus.and.parse(files = "all")

# computing a list of most frequent words (trimmed to top 2000 items):
features <- make.frequency.list(tokenized.texts, head = 100)
#This computation only needs to be done once, and generates the vectors actually used.

# producing a table of relative frequencies:
data <- make.table.of.frequencies(tokenized.texts, features, relative = TRUE)

settings <- stylo.default.settings()

results <- data.frame(matrix(nrow = 0, ncol = 4))

colnames(results) <- c("user", "is_perfect", "position", "users_considered")

#Note that R automatically wraps the table, but each author only has one row

# who wrote "Pride and Prejudice"? (in my case, this is the 4th row in the table):
print(nrow(data))
print(str(class(data)))
print("Iterating")
for(n in seq_along(data))
{
    if (n == 0 | n == rows)
    {
        continue
    }
    al <- imposters(reference.set = data[1:n-1,] + data[n+1: nrow(data),], test = data[n,], distance = "wurzburg", features = 1.0, imposters = 1.0)
}
print("Done Iterating")

print(n["Griffs"])