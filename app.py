from flask import Flask, render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
import re
import nltk
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords

app = Flask(__name__)


def normalization(text):
    processed_text = re.sub(f"[{re.escape(punctuation)}]", "",text)
    processed_text = " ".join(processed_text.split())
    return processed_text

# Lemmatization

def Lemmatization(text):
    wordnet_lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
#     print(tokens)
    required_words = [wordnet_lemmatizer.lemmatize(x, 'v') for x in tokens]
#     print(required_words)
    return required_words

# stop word removal

def stop_word_removal(word):
    stop_words = set(stopwords.words('english'))
    filtered_words = [x for x in word if x not in stop_words]
#     without_stop_words = " ".join(filtered_words)
    return filtered_words

# pos tagging

def create_pos_tags(required_words):
    sent = nltk.pos_tag(required_words)
    return sent


# ...

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        nor_query = normalization(query)
        lem_query = Lemmatization(nor_query)
        final_query = create_pos_tags(lem_query)
        cla = [i[0] for i in final_query if i[1] == 'NNS']
        data_prop = [i[0] for i in final_query if i[1] == 'NN']
        
        # Pass cla and data_prop to the run_query function
        return render_template('result.html', query=query, results=run_query(cla, data_prop), nor_query=nor_query,  lem_query=lem_query, final_query=final_query)
    return render_template('index.html')

# Modify run_query function to accept cla and data_prop as arguments
def run_query(cla, data_prop):
    sparql = SPARQLWrapper("http://localhost:3030/HospitalityProject/query")
    # Check if any desired amenity exists in data_prop
    amenities_to_check = ["roomservice", "gym", "swimmingpool", "spa", "loungearea", "laundry"]
    has_desired_amenity = any(amenity.lower() in amenities_to_check for amenity in data_prop)

    # Check for menu items in data_prop
    menu_items_to_check = ["Dessert", "appetizer"]
    has_menu_items = any(amenity.lower() in menu_items_to_check for amenity in data_prop)

    #check the data of guest
    guest_list_to_check = ["hotel","guests","guest","bill"]
    has_guest = any(amenity.lower() in guest_list_to_check for amenity in data_prop)

    # Define filter_condition1 for amenities
    filter_condition1 = ""
    if has_desired_amenity:
        filter_condition1 = f"FILTER(?Price=\"yes\")"

    # Define filter_condition2 for menu items
    filter_condition2 = ""
    if has_menu_items:
        filter_condition2 = f"OPTIONAL {{ ?sub hp:has_desert ?des. ?des hp:name ?Desert. }}"

        # Combine filter_conditions
    filter_condition = filter_condition1 + " " + filter_condition2



    sparql.setQuery(f"""
    PREFIX hp:<http://www.HospitalityServices.com/HospitalityServices#>
    SELECT ?name ?Price ?Desert ?des ?hname
    WHERE {{
        ?sub a hp:{cla[0]}.
        ?sub hp:{data_prop[0]} ?name.
        ?sub hp:{data_prop[1]} ?Price.
        OPTIONAL{{?sub hp:staysinhotel 
        ?hotel. ?hotel hp:name ?hname.}}
        {filter_condition}
    }}
        ORDER BY ASC(?Price)
""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']

if __name__ == '__main__':
    app.run(debug=True)
