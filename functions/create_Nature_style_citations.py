# diferenciate between number of authors

# 1: Author e.g. FitzGerald, G. A. + Title + Journal + volume + pages + (year)

# 2: Yuan, Q. & Zhao, Y.-P.  (all same but autors are seperated with &)

# 3-5: Yurtsever, A., van der Veen, R. M. & Zewail, A. H.  (last autor sep. with &)

# 6 or more: Mikołajczyk-Stecyna, J. et al.  only first autor with et al.

# https://paperpile.com/s/nature-citation-style/

def reformat_author(author_s):
    if len(author_s) == 1:

        split = author_s[0].split(' ')

        if len(split) == 2:
            first_letters = str()
            for ele in split[1]:
                first_letters += ' ' + ele + '.'
            return [split[0] + ',' + first_letters]

        elif len(split) > 2:
            first_letters = str()
            first_part = ' '.join(split[0:-1])
            for ele in split[-1]:
                first_letters += ' ' + ele + '.'
            return [first_part + ',' + first_letters]

    else:
        author_list = list()

        for author in author_s:

            split = author.split(' ')

            if len(split) == 2:
                first_letters = str()
                for ele in split[1]:
                    first_letters += ' ' + ele + '.'
                author_list.append(split[0] + ',' + first_letters)

            elif len(split) > 2:
                first_letters = str()
                first_part = ' '.join(split[0:-1])
                for ele in split[-1]:
                    first_letters += ' ' + ele + '.'
                author_list.append(first_part + ',' + first_letters)

        return author_list


def nature_citation(fetched_article):

    authors = fetched_article.authors
    authors = reformat_author(authors)

    # create citation body without authors (since this part is always the same)
    title = fetched_article.title
    journal = fetched_article.journal
    journal = '. '.join(journal.split(' '))+'.'
    volume = fetched_article.volume
    pages = fetched_article.pages
    year = fetched_article.year

    cite_body = f'{title} {journal} {volume}, {pages} ({year})'

    if len(authors) == 1:
        return authors[0] + ' ' + cite_body + '.'

    elif len(authors) == 2:
        return authors[0] + ' & ' + authors[1] + ' ' + cite_body + '.'

    elif len(authors) > 2 and len(authors) < 6:
        return ', '.join(authors[0:-1]) + ' & ' + authors[-1] + ' ' + cite_body + '.'

    elif len(authors) >= 6:
        return authors[0] + ' et al.' + ' ' + cite_body + '.'








if __name__ == '__main__':
    from metapub import PubMedFetcher

    test_id = '34326236'
    fetch = PubMedFetcher()

    # author test
    article = fetch.article_by_pmid(test_id)
    author_s = article.authors
    print(nature_citation(article))
