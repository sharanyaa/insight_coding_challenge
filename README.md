Insight Data Engineering - Coding Challenge
===========================================================
Submitted by: SHARANYA RADHAMOHAN radhamoh@usc.edu
===========================================================
Language/Environment: Python 3
Libraries: Standard Python libraries (sys, fileinput, os.path, json, collections, string, re)

tweets_cleaned.py:
- Generates feature 1 as required by the Insight Challenge description.
- Tweets are cleaned by removing unicode non-ascii characters and replacing all escaped whitespace characters with a space and written into the output file.

average_degree.py:
- Generates feature 2 as required by the Insight Challenge description.
- A graph is built using the hashtags extracted from the tweets and average degree is calculated and written into the output file as each new tweet is processed.

run.sh:
- Executes tweets_cleaned.py using input file and writes into output file
- Next, runs average_degree.py using input file and writes into output file
- Run the script as ./run.sh from the root directory

TO RUN tweets_cleaned.py: python3 src/tweets_cleaned.py INPUT_FILE_PATH OUTPUT_FILE_PATH
TO RUN average_degree.py: python3 src/average_degree.py INPUT_FILE_PATH OUTPUT_FILE_PATH

