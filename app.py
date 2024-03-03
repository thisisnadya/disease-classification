from flask import Flask, request, render_template
import os
import nltk
import pickle
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


# modules made by self
from modules.data_processing import process_data, calculate_frequencies, load_data, process_data2, count_address, age_group
from modules.data_visualization import generate_plot_category, generate_plot_address, generate_plot_age_group, generate_word_cloud
from modules.text_processing import clean_text, calculate_word_freq

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

current_dir = os.path.dirname(__file__)
app = Flask(__name__)

model = pickle.load(open('./res/knn_model.pickle', 'rb')) # model used for prediction
cv = pickle.load(open('./res/bow.pickle', 'rb')) # count vectorizer to transform the clean input into bag of words

# load data
excel_file_path = os.path.join(current_dir, 'res', 'Merged_All_Fixed.xlsx')

# load data
df = load_data(excel_file_path)

# process data for count most freq categories
df1 = process_data(df)
most_freq_category = calculate_frequencies(df1)
plot_category= generate_plot_category(most_freq_category)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get the input
        input_text = request.form['input_text']
        
        # preprocess the input
        preprocessed_text = clean_text(input_text)

        print(preprocessed_text)

        # Concatenate the list of strings into a single string
        # preprocessed_text = ' '.join(preprocessed_text)

        # transform the input into bag of words
        bow_input = cv.transform([preprocessed_text])

        # make a classification
        target_class = model.predict(bow_input)[0]
        print(target_class)

        # Map predicted label to corresponding category
        label_map = {
            1: '[J] Penyakit pada sistem respirasi',
            2: '[R] Gejala, tanda, hasil abnormal dari prosedur klinis atau prosedur investigasi lainnya (Perlu Pemeriksaan Lebih Lanjut)',
            3: '[I] Penyakit pada sistem peredaran darah',
            4: '[K] Penyakit pada sistem pencernaan'
        }

        prediction = label_map.get(target_class, 'Lainnya. Perlu Pemeriksaan Lebih Lanjut')

        return render_template('result.html', preprocessed_text=preprocessed_text, plot_category=plot_category, plot_address=plot_address, plot_age_group=plot_age_group, plot_wordcloud=plot_wordcloud, target_class=prediction)

    return render_template('index.html', plot_category=plot_category, plot_address=plot_address, plot_age_group=plot_age_group, plot_wordcloud=plot_wordcloud)

if(__name__)=='__main__':
    app.run(debug=True)