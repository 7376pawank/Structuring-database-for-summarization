import docx
import json
import functions_for_data_extraction

file_contents = []
data_extracted=[]
avg_headnotes = 0
avg_judgements=0

# Loop through the file numbers
for i in range(1, 10001):
    file_name = f"Judgements/{i}.docx"  # Assuming the file names follow the pattern 'file1.docx', 'file2.docx', and so on

    try:
        # Open the Word file
        doc = docx.Document(file_name)

        # Read the paragraphs and join them into a single string
        paragraphs = [p.text for p in doc.paragraphs]
        content = '\n'.join(paragraphs)

        # Append the content to the list
        print(i)
        file_contents.append(functions_for_data_extraction.combine_hyphenated_words(content))
        json_extract, len_of_hednotes, len_of_judgement = functions_for_data_extraction.json_data_func(file_contents[i-1])
        json_data = json.dumps(json_extract, indent=4)
        data_extracted.append(json_data)
        avg_headnotes = avg_headnotes+len_of_hednotes
        avg_judgements = avg_judgements+len_of_judgement

    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
print("mean headnotes sentences", int(avg_headnotes/10000))
print("mean judgement sentences", int(avg_judgements/10000))

#CREATION OF JSON DATASET
with open("data.json", "w") as json_file:
    json.dump(data_extracted, json_file, indent=4)

with open("data1.json", "r") as json_file:
    dictionaries = json.load(json_file)

