import re
import pandas as pd
from metapub import PubMedFetcher
import copy
import os


root_dir = '/'.join(os.path.dirname(os.path.abspath(__file__)).replace('/', '\\').split('\\'))

data_dir = root_dir + '/Data'

write_lib = data_dir + '/test_lib.txt'
write_text = data_dir + '/test_text.txt'

text = open(data_dir + '/covid_art.txt','r').read()

# init out format
id_frame = pd.DataFrame(columns=['line', 'PMID', 'label', 'Citation'])

# init fetcher
fetch = PubMedFetcher()

# fill per line pmids in df
for idx, line in enumerate(text.split("\n")):
    # buffer var to collect elements per line
    idBuffer = list()
    idBuffer += re.findall("PMID(\d{6,8})", line)
    idBuffer += re.findall("pmid:(\d{6,8})", line)
    idBuffer += re.findall("pmid: (\d{6,8})", line)

    if len(idBuffer) == 1:
        add_line = len(id_frame) + 1
        id_frame.loc[add_line, 'line'] = idx + 1
        id_frame.loc[add_line, 'PMID'] = idBuffer[0]
        id_frame.loc[add_line, 'Citation'] = fetch.article_by_pmid(idBuffer[0]).citation

    elif len(idBuffer) > 1:
        for id in idBuffer:
            add_line = len(id_frame) + 1
            id_frame.loc[add_line, 'line'] = idx + 1
            id_frame.loc[add_line, 'PMID'] = id
            id_frame.loc[add_line, 'Citation'] = fetch.article_by_pmid(id).citation


# give every pmid an index in order of appearance in the text
for idx, row in id_frame.iterrows():
    if row['PMID'] not in list(id_frame.loc[1:idx-1, 'PMID']):
        id_frame.loc[idx, 'label'] = idx
    elif row['PMID'] in list(id_frame.loc[1:idx-1, 'PMID']):
        try:
            id_frame.loc[idx, 'label'] = id_frame.loc[1:idx-1].loc[id_frame['PMID'] == row['PMID'], 'label'].item()
        except ValueError:
            min_match_index = min(id_frame.loc[id_frame['PMID'] == row['PMID'], 'label'])
            id_frame.loc[idx, 'label'] = id_frame.loc[min_match_index,'label']


# updating text with references
updated_text = copy.deepcopy(text)
for idx, row in id_frame.iterrows():
    updated_text = updated_text.replace('pmid:'+row['PMID'], str(row['label'])).replace('pmid: '+row['PMID'], str(row['label']))

# creating lib
lib = str()

for idx, row in id_frame.drop_duplicates(subset=['label']).iterrows():
    lib += f'[{row["label"]}] {row["Citation"]}\n'

# create file with edited text
text_file = open(write_text,'w')
text_file.write(updated_text)
text_file.close()

# create a Bibliography file
lib_file = open(write_lib,'w')
lib_file.write(lib)
lib_file.close()
