import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bokeh.plotting import figure
from bokeh.embed import components
from io import BytesIO
import base64

def generate_plot_freq_category(most_freq_category):
    plt.figure(figsize=(8,4))
    # Generate plot using most_freq_category data
    fig = most_freq_category['Count'].plot(kind="bar", width=0.8, color="#4F709C")
    fig.set_xticklabels(most_freq_category['Letter'])
    fig.bar_label(fig.containers[0], label_type='edge')

    # add padding
    plt.tight_layout()

    # remove top and right border
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.gcf().set_facecolor('None')
    # plt.show()

    # Convert plot to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data_most_category = base64.b64encode(buffer.getvalue()).decode()

    return plot_data_most_category

# def generate_plot_category(most_freq_category):
#     # create a bokeh figure
#     p = figure(x_range=most_freq_category['Letter'], height=350, toolbar_location=None, tools="")

#     # add bars to the plot
#     p.vbar(x='Letter', top='Count', width=0.9, source=most_freq_category, line_color='white', fill_color='blue')

#     # customize plot properties
#     p.xaxis.major_label_orientation = 1.2

#     # convert the plot to components
#     script, div = components(p)

#     return script, div

def generate_plot_address(df_count_alamat):

    plt.clf()
    plt.figure(figsize=(5,3))
    # visualize alamat terbanyak
    colors = ["#226089", "#427D9D", "#9BBEC8", "#B6C4B6", "#9EB8D9"]

    # plot in pie chart
    _, _, texts = plt.pie(df_count_alamat['Count'], colors=colors, autopct='%1.1f%%')

    [text.set_color('white') for text in texts]

    # Create legend based on df_count_alamat['Kecamatan']
    plt.legend(df_count_alamat['Kecamatan'], loc='center left', bbox_to_anchor=(-0.6, 0.5))
    plt.gcf().set_facecolor('None')
    # plt.show()

    # Convert plot to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data_address = base64.b64encode(buffer.getvalue()).decode()

    return plot_data_address

def generate_plot_age_group(df_age_range_counts):
    plt.clf()

    plt.figure(figsize=(4,2))

    df_age_range_counts.plot(kind='bar', color='#34626C')
    plt.xlabel("Kategori usia")
    plt.ylabel("Banyak pasien")
    plt.xticks(rotation=0)

    # remove top and right border
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.gcf().set_facecolor('None')
    # plt.show()

    # Convert plot to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_age_group = base64.b64encode(buffer.getvalue()).decode()

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
