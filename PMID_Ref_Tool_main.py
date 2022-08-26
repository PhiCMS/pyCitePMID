import os
from functions import get_PMIDS, replace_pmid_in_text, create_bib

if __name__ == '__main__':

    # define project path
    root_dir = '/'.join(os.path.dirname(os.path.abspath(__file__)).replace('/', '\\').split('\\'))

    data_dir = root_dir + '/Data'

    # load sample text
    text = open(data_dir + '/sampel_text.txt','r').read()


    # define save file path(s)
    write_lib = data_dir + '/lib.txt'
    write_text = data_dir + '/replaced_text.txt'

    # extract pmids with the standard regEx settings
    # Currently covered PMID<ID>; PMID:<ID>; PMID: <ID>; pmid<ID>; pmid:<ID>, pmid: <ID>
    frame = get_PMIDS.fetch_pmid_cites(text, customReX=None)

    # crate new .txt with replaced pmids
    replace_pmid_in_text.update_text(text,frame, write_text)

    # create new .txt with the bib
    create_bib.create_bibliography(frame, write_lib)