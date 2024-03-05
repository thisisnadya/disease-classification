import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
from bokeh.plotting import figure
from bokeh.embed import components
from io import BytesIO
import base64

def generate_plot_category(most_freq_category):
    fig = px.bar(most_freq_category, x='Kategori', y='Jumlah', hover_data=['Jumlah'], color_discrete_sequence=['#4F709C'], template='plotly')


    plot_data_freq_category = fig.to_json()

    return plot_data_freq_category

def generate_plot_address(df_count_alamat):
    # create pie chart with hover tooltips
    fig = px.pie(df_count_alamat, values='Count', names='Kecamatan', hover_data=['Count'], color_discrete_sequence=["#226089", "#427D9D", "#9BBEC8", "#B6C4B6", "#9EB8D9"], width=400, height=400)

    plot_data_address = fig.to_json()

    return plot_data_address


def generate_plot_age_group(df_age_range_counts):
    fig = px.bar(df_age_range_counts, x='Kategori', y='Jumlah', color_discrete_sequence=['#34626C'], width=500, height=400)

    plot_age_group = fig.to_json()
    return plot_age_group
    
def generate_word_cloud(word_freq):
    plt.clf()
    word_freq_dict = dict(word_freq)
    wordcloud_generate = WordCloud(width=400, height=300, background_color='rgba(255, 255, 255, 0)').generate_from_frequencies(word_freq_dict)


    plt.figure(figsize=(4, 2))

    plt.imshow(wordcloud_generate, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()  # Ensure tight layout for responsive resizing
    plt.gcf().set_size_inches(4.5, 4)  # Set a default size, which can be adjusted by CSS
    # plt.show()

    # Convert plot to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_wordcloud = base64.b64encode(buffer.getvalue()).decode()
    
    return plot_wordcloud
