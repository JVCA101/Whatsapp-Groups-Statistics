import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
def plot_counts(data_dict, users, font_size=12):
    for key in data_dict.keys():
        # print(f"{key}: {data_dict[key]}")
        df = pd.DataFrame(data_dict[key], index=users)
        ax = df.plot.bar(title=f"{key} enviados por pessoa", rot=0, legend=False, fontsize=font_size)
        fig = ax.get_figure()
        fig.savefig(f"./count_{key.split(' ')[-1].lower()}.png")
    df = pd.DataFrame(data_dict, index=users)
    ax = df.plot.bar(title="Quantidade de mensagem, mídias e emojis enviados por pessoa", rot=0, legend=True, fontsize=font_size)
    fig = ax.get_figure()
    fig.savefig("./count_all.png")

def process_output(dir: str):
    os.chdir(dir)
    with open("people_stat.txt", 'r') as output_file:
        info = []
        for line in output_file:
            parameters = line.split(";")[:-1]
            print(parameters)
            info.append(parameters)

        user_dictionary = {name: {
                            "messages_count": int(messages_count),
                            "media_count": int(media_count),
                            "emojis_count": int(emojis_count),
                            "kkks_sum": int(kkks_sum),
                            "kkks_max": int(kkks_max),
                            "kkks_min": int(kkks_min),
                            "kkks_median": float(kkks_median),
                            "kkks_avg": float(kkks_avg)
                            } for name, messages_count, media_count, emojis_count, kkks_sum, kkks_max, kkks_min, kkks_median, kkks_avg in info}
        # print(user_dictionary)
        font_size = 12
        data_dict = {"Quantidade de mensagens": [],
                     "Quantidade de midias": [],
                     "Quantidade de emojis": []}
        
        for user in user_dictionary:
            data_dict["Quantidade de mensagens"].append(user_dictionary[user]["messages_count"])
            data_dict["Quantidade de midias"].append(user_dictionary[user]["media_count"])
            data_dict["Quantidade de emojis"].append(user_dictionary[user]["emojis_count"])

        kkks_dict = {"Máximo de kkks": [],
                     "Mínimo de kkks": [],
                     "Média de kkks": []}
        for user in user_dictionary:
            kkks_dict["Máximo de kkks"].append(user_dictionary[user]["kkks_max"])
            kkks_dict["Mínimo de kkks"].append(user_dictionary[user]["kkks_min"])
            kkks_dict["Média de kkks"].append(user_dictionary[user]["kkks_avg"])

        plot_counts(data_dict, user_dictionary.keys(), font_size)

    with open("emoji_hash.txt", 'r') as emoji_file:
        emoji_total = 0
        emojis = []
        counts = []
        for line in emoji_file:
            emoji_char, count = line.split(":")
            emoji_total += int(count)
            if int(count) >= 2:
                emojis.append(emoji_char)
                counts.append(int(count))
        print(emojis)
        data_dict = {"Frequência de Emojis": counts}
        
        sizes = counts
        labels = emojis
        # colors = ['red', 'yellow', 'green', 'blue'] # Optional: define custom colors
        # explode = [0.1, 0, 0, 0] # Optional: "explode" the first slice

        
        def my_autopct(pct):
            # Calculate the actual value from the percentage
            absolute_value = int(round(pct * emoji_total / 100.0))
            # Only return the string if the percentage is above the threshold (e.g., 15%)
            if pct > 3.0:
                return "{:.1f}%".format(pct)
            else:
                return ""
            
        # Create the pie chart
        font_path = "../font/NotoColorEmoji.ttf"
        custom_font_prop = fm.FontProperties(fname=font_path)

        plt.clf()
        patches, texts, autotext = plt.pie(sizes, 
                labels=labels,
                autopct=my_autopct, # Add percentage labels
                startangle=90)

        # Iterate over the text objects and set the font family
        for text in texts:
            text.set_fontproperties(custom_font_prop)
        plt.title("Frequência de Emojis", fontsize=font_size)
        plt.savefig("./emoji_frequency.png")

        # df = pd.DataFrame(data_dict, index=emojis)
        # ax = df.plot.pie(title="Frequência de Emojis", y="Frequência de Emojis", legend=False, fontsize=font_size)
        # fig = ax.get_figure()
        # fig.savefig("./emoji_frequency.png")
    
    print("")
    os.chdir("../")

def main():
    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir) and not dir.startswith("."):
            process_output(dir)

if __name__ == "__main__":
    main()
