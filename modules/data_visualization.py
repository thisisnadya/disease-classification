import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from io import BytesIO
import base64

def generate_plot_freq_category(most_freq_category):
    plt.figure(figsize=(8,4))
    # Generate plot using most_freq_category data
    fig = most_freq_category['Count'].plot(kind="bar")
    fig.set_xticklabels(most_freq_category['Letter'])
    fig.bar_label(fig.containers[0], label_type='edge')
    plt.gcf().set_facecolor('None')
    # plt.show()

    # Convert plot to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data_most_category = base64.b64encode(buffer.getvalue()).decode()

    return plot_data_most_category

def generate_plot_address(df_count_alamat):

    plt.clf()
    plt.figure(figsize=(5,3))
    # visualize alamat terbanyak
    colors = ["green", "yellow", "lightcoral", "blue", "magenta"]

    # plot in pie chart
    plt.pie(df_count_alamat['Count'], colors=colors, autopct='%1.1f%%')

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

    df_age_range_counts.plot(kind='bar', color='blue')
    plt.title("Distribusi usia pasien")
    plt.xlabel("Kategori usia")
    plt.ylabel("Banyak pasien")
    plt.xticks(rotation=0)
    plt.gcf().set_facecolor('None')
    # plt.show()

    # Convert plot to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_age_group = base64.b64encode(buffer.getvalue()).decode()

    return plot_age_group

def generate_word_cloud(word_freq):
    word_freq_dict = dict(word_freq)
    wordcloud_generate = WordCloud(width=450, height=300, background_color="white").generate_from_frequencies(word_freq_dict)

    plt.clf()

    plt.figure(figsize=(5, 4))
    plt.imshow(wordcloud_generate, interpolation='bilinear')
    plt.axis('off')
    # plt.show()

    # Convert plot to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_age_group = base64.b64encode(buffer.getvalue()).decode()
    
    return plot_age_group
