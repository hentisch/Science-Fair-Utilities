# Science-Fair-Utilities
A collection of the code used in my 2022 Science Fair Project. A slideshow representing the details and results of this experiment can be found [here](https://docs.google.com/presentation/d/1eHU47d5N7uJEQOwiM-YNiEXEwjyVUadOiPHeUgPeXpY/edit?usp=sharing). Raw results can be found in this projects "recorded_data folder"

### Project Abstract
  As social media grows, so does its potential for exploitation, and with this the need for effective moderation grows. A primary issue, often rendering moderation ineffective is the ease of which one individual can use and operate many separate accounts. This research makes use of common stylometric methods - able to look at one's individual, abstract writing style - in order to identify a social media account simply by how they write, potentially bypassing the natural limitations of digital identifiers.
  To benchmark the capabilities of stylometry, the general imposters method was used. For each user, their writings were split into two parts, one then “hidden” amongst other random writings. Then, the tested algorithm was used to find the stylistic difference between all considered text segments. The performance of the algorithm was measured by the ranking, amongst all text segments, that the “hidden” element received. The highest performing algorithm reached an average ranking of 27.5/399 for the “hidden" text, and a total accuracy of 49%.
  This experiment successfully demonstrates the basic capabilities of stylometry when applied to social media. However, while able to provide a general direction of authorship, stylometry falls short when trying to identify an exact author.

### Usage
This code was used to conduct a single experiment and as such this repository does not represent a single program or "thing" (besides, of course, this experiment) the code is simply here in the spirit of scientific openness, and in case someone may find it usefull. However, the generall flow of of scripts used for this experiment relies on using Profile_Downloader.py to download reddit users, and imposters_testing.py to perform the experiment. There are, of course, many more class files however these are the two scripts one would need to run to conduct the experiment.

Feel free to contact me at henrygtischler@gmail.com for any further questions or specifications with the project.
