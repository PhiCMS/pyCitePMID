## Just planned for later versions


def get_NLM_cite(fetched_article):
    print('stuff')


if __name__ == '__main__':
    from metapub import PubMedFetcher

    test_id = '33233837'
    fetch = PubMedFetcher()
    article = fetch.article_by_pmid(test_id).citation

    # just the order of appearance in the NLM style citation
    article.authors
    article.title
    article.journal
    article.year
    ##
    article.volume_issue
    article.pages
    article.doi
    article.pmid
    article.pmc





