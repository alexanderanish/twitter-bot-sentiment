import matplotlib.pyplot as plt

def sentimentPlotImage(bear,bull,stock):
    labels = ['Bearish', 'Bullish']
    sentiments = [bear, bull]


    width = 0.35       # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(labels, sentiments, width, color=['#a8030e','#0f6927'])

    title="Sentiment for {}".format(stock)
    filename="{}.png".format(stock)
    ax.set_ylabel('Percentage')
    ax.set_title(title)
    plt.savefig(filename)
    #plt.show()
    return filename

if __name__ == '__main__':
    sentimentPlotImage(30,40,"APPL")