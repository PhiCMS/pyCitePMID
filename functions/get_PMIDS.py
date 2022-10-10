import re
import pandas as pd
from metapub import PubMedFetcher
import time
from functions.create_Nature_style_citations import nature_citation


def fetch_pmid_cites(text, pause_dur=3,customReX=None):

    '''
    :param text: text file as string
    :param pause_dur: how long the program should pause between requests. Without NCBI API Key its limited
                        to 3 requests per sec. more at: (https://pypi.org/project/metapub/)
    :param customReX: Custom regular expression string to find the pubmed ids
    :return: pandas data frame containing line of appearance, PMID, Label as running index for order of appearance
            (does consider multi appearing ids), Citation as got from the pubmed server
    '''

    # init out format
    id_frame = pd.DataFrame(columns=['line', 'PMID', 'label', 'Citation'])

    # init fetcher
    fetch = PubMedFetcher()

    # fill per line pmids in df
    for idx, line in enumerate(text.split("\n")):
        # buffer var to collect elements per line
        idBuffer = list()

        if not customReX:
            # Currently covered PMID<ID>; PMID:<ID>; PMID: <ID>; pmid<ID>; pmid:<ID>, pmid: <ID>
            idBuffer += re.findall("PMID(\d{6,8})", line)
            idBuffer += re.findall("PMID: (\d{6,8})", line)
            idBuffer += re.findall("PMID:(\d{6,8})", line)
            idBuffer += re.findall("pmid(\d{6,8})", line)
            idBuffer += re.findall("pmid:(\d{6,8})", line)
            idBuffer += re.findall("pmid: (\d{6,8})", line)

        else:
            idBuffer += re.findall(customReX, line)


        if len(idBuffer) == 1:
            add_line = len(id_frame) + 1
            id_frame.loc[add_line, 'line'] = idx + 1
            id_frame.loc[add_line, 'PMID'] = idBuffer[0]
            id_frame.loc[add_line, 'Citation'] = nature_citation(fetch.article_by_pmid(idBuffer[0]))
            time.sleep(pause_dur)

        elif len(idBuffer) > 1:
            for id in idBuffer:
                add_line = len(id_frame) + 1
                id_frame.loc[add_line, 'line'] = idx + 1
                id_frame.loc[add_line, 'PMID'] = id
                id_frame.loc[add_line, 'Citation'] = nature_citation(fetch.article_by_pmid(id))
                time.sleep(pause_dur)


    # give every pmid an index in order of appearance in the text
    counter = 0
    for idx, row in id_frame.iterrows():
        if row['PMID'] not in list(id_frame.loc[1:idx-1, 'PMID']):
            counter += 1
            id_frame.loc[idx, 'label'] = counter
        elif row['PMID'] in list(id_frame.loc[1:idx-1, 'PMID']):
            try:
                id_frame.loc[idx, 'label'] = id_frame.loc[1:idx-1].loc[id_frame['PMID'] == row['PMID'], 'label'].item()
            except ValueError:
                min_match_index = min(id_frame.loc[id_frame['PMID'] == row['PMID'], 'label'])
                id_frame.loc[idx, 'label'] = id_frame.loc[min_match_index,'label']

    return id_frame