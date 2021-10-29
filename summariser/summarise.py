import openai
import requests
import json
import os
from bs4 import BeautifulSoup


openai.api_key = os.getenv("OPENAI_SECRET_KEY")

class Summariser:
    def __init__(self, temperature, max_tokens):
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, input):
        """
        pre-appends default intro and outro to prompt

        :param input: text to summarise
        :return: summarised json formatted text
        """
        start = "My university friend asked me to summarise what this passage means: \n\n"
        body = "\"\"\"" + input + "\"\"\"\n\n"
        end = "I rewrote the article in the following bullet points:" + "\"\"\"\n"
        prompt = start + body + end
        return openai.Completion.create(engine="davinci", prompt = prompt, max_tokens = self.max_tokens)

    def get_only_text(self, url):
        """
        return the text of the article( only extracts p tags)
        at the specified url
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "lxml")
        text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
        return text

    def get_text_summary(self, url):
        """

        :param url: url to extract text from
        :return: summarised text from url(json formatted)
        """
        prompt = self.get_only_text(url)
        return self.generate(prompt)

    def extract_text_summary(self, url):
        """

        :param url: url to extract text from
        :return: strip irrelevant tags and only returns text summary(normal paragraph or bullet points)
        """
        text_summary = self.get_text_summary(url)
        json_dict = json.loads(json.dumps(text_summary))
        return json_dict['choices'][0]['text']





#test out
"""
input:

Original text: 

Good Food reader Charlotte Hilsdon shares her simple, chocolate chip muffin recipe, to which you 
can add fruit, chocolate or nuts Heat oven to 200C/180C fan/gas 6. Line 2 muffin trays with paper muffin cases.
In a large bowl beat 2 medium eggs lightly with a handheld electric mixer for 1 min. Add 125ml
vegetable oil and 250ml semi-skimmed milk and beat until just combined then add 250g golden
caster sugar and whisk until you have a smooth batter. Sift in 400g self-raising flour and 1 tsp salt
(or 400g plain flour and 3 tsp baking powder if using) then mix until just smooth. Be careful not to over-mix
the batter as this will make the muffins tough. Stir in 100g chocolate chips or dried fruit if using.
Fill muffin cases two-thirds full and bake for 20-25 mins, until risen, firm to the touch and a skewer
inserted in the middle comes out clean. If the trays will not fit on 1 shelf, swap the shelves around
after 15 mins of cooking. Leave the muffins in the tin to cool for a few mins and transfer to a wire rack to
cool completely. Use code: Dedica685 and Save £15 on the De’Longhi “EC 685.M” coffee machine.
-------------------------

output:

Summarised text:

1. Beat eggs until foamy.

2. Beat in oil, milk, lemon zest, vanilla extract, cinnamon, nutmeg, cloves, half the sugar, self-raising flour and salt.

3. Stir in chocolate chips, fresh fruit or chopped nuts. Fill muffin cases ⅔ full.

4. Bake for 20-25 mins. If multiple trays will not fit on 1 shelf, swap halfway through cooking.

5. Leave

"""

#test summary output


summarise = Summariser(0, 100)
test_url = "https://www.bbcgoodfood.com/recipes/basic-muffin-recipe"

print("Original text: \n")
print(summarise.get_only_text(test_url))

print("-------------------------\n\n Summarised text:\n")
print(summarise.extract_text_summary(test_url))


