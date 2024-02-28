from flask import Flask, request, render_template
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import pickle
import modules.data_processing as dp

from modules.data_processing import process_data, calculate_frequencies, load_data, process_data2, count_address, age_group
from modules.data_visualization import generate_plot_freq_category, generate_plot_address, generate_plot_age_group, generate_word_cloud
from modules.text_processing import clean_text, calculate_word_freq

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

current_dir = os.path.dirname(__file__)
app = Flask(__name__)

# model = pickle.load(open('nb_model.pickle', 'rb'))

# load data
excel_file_path = os.path.join(current_dir, 'res', 'Merged_All_Fixed.xlsx')

@app.route('/', methods=['GET', 'POST'])
def index():
    # load data
    df = load_data(excel_file_path)

    # process data for count most freq categories
    df1 = process_data(df)
    most_freq_category = calculate_frequencies(df1)
    plot_category = generate_plot_freq_category(most_freq_category)

    # process data for most symptomps in the form of wordcloud
    word_freq = calculate_word_freq(df1)
    plot_wordcloud = generate_word_cloud(word_freq)

    # process data for another mining
    df2 = process_data2(df)

    # count address percentage
    address_percentage = count_address(df2)
    plot_address = generate_plot_address(address_percentage)

    # create age group
    count_age_group = age_group(df2)
    plot_age_group = generate_plot_age_group(count_age_group)

    
    if request.method == 'POST':
        # get the input
        input_text = request.form['input_text']
        
        # preprocess the input
        preprocessed_text = clean_text(input_text)

        return render_template('result.html', preprocessed_text=preprocessed_text, plot_category=plot_category, plot_address=plot_address, plot_age_group=plot_age_group, plot_wordcloud=plot_wordcloud)

    return render_template('index.html', plot_category=plot_category, plot_address=plot_address, plot_age_group=plot_age_group, plot_wordcloud=plot_wordcloud)

if(__name__)=='__main__':
    app.run(debug=True)