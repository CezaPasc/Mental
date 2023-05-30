import os
import pandas as pd
import numpy as np

naming_convetion = {
    "tweet": "text",
    "Tweet": "text",
    "post": "text",
    "body": "text",
    "target": "label",
    "boolean": "label",
    "class_id": "label",
}


if __name__ == "__main__":
    path = "Mental/data/scrapped/new"

    datasets = []

    label_number = 1
    labels = {}
    for f in os.listdir(path):
        print(f)
        if not f.endswith(".csv"):
            print("its not a csv")
            continue

        name = f.replace(".csv", "")
        name = name.replace("more_", "")
        if "combined" in name:
            continue

        file_path = path + "/" + f
        df = pd.read_csv(file_path)
        df = df.rename(columns=naming_convetion)
        df = df[["text", "label"]]

        if name == "negative_samples":
            df["label"] = "0"
        else:
            if name in labels:
                df["label"] = labels[name]
            else:
                df["label"] = str(label_number)
                labels[name] = str(label_number)
                label_number += 1

        df["label_name"] = name
        df = df.dropna()
        datasets.append(df)

    total = pd.concat(datasets)

    print(total.groupby("label_name")["text"].count())

    train, validation, test = np.split(total.sample(frac=1), [int(0.6*len(total)), int(0.8*len(total))])

    train.to_csv(path + "/t_combined_train.csv", index=False)
    validation.to_csv(path + "/t_combined_val.csv", index=False)
    test.to_csv(path + "/t_combined_test.csv", index=False)v
