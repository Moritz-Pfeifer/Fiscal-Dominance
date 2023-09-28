# Preprocessing 

This script removes stopwords and uses a regular expression to 

1) find and replace URLs and web addresses with a space. It effectively removes URLs from the text.
2) convert all text to lowercase. 
3) remove non-word characters (e.g., punctuation and special characters) and replaces them with spaces.
4) remove digits (numbers) from the text and replaces them with spaces.
5) remove single characters (letters) that are surrounded by spaces.
6) remove single characters (letters) at the end of a line if they are preceded by a space.
7) remove single characters (letters) at the beginning of a line if they are followed by a space.
8) remove multiple consecutive spaces and replaces them with a single space, effectively normalizing spaces between words.






