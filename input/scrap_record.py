from bs4 import BeautifulSoup as BS
import re


def split_pair_occurrence(input_str):
    """
    Q9HD36.A79T (x11) → (Q9HD36.A79T, 11)
    TODO: fill doc string.
    """
    if '(x' not in input_str:
        return input_str, 1

    pair, occurrence = [item.strip() for item in input_str.split()]
    occurrence = int(occurrence[2:-1])

    return pair, occurrence


def get_stripped_error_title(error_str):
    """Get rid of paranthesis and numbers within."""
    error_title = re.sub(r"\((\d+)\)" + ":", '', error_str).strip()
    return error_title


def count_duplicates(values):
    """Counting the number of duplicates."""
    return sum([split_pair_occurrence(value)[1] for value in values])


def process_single_error(html_text):
    """
        Processes single error with its title and values.

        Parameters
        ----------
            html_text : <str>
                The HTML text which contains information to be scrapped.

        Returns
        -------
            error_title : <str>
                Error title, e.g. Invalid syntax.

            values : <list>
                Error values, e.g. ['Q9HD36.A79T', 'Q9ULH7.G370R']

            num_values : <int>
                Number of error values.
                If Error title is `Duplicated`, then it counts the number of total occurrences.
                    e.g. ['Q06418.A379T (x3)'] → 3.
                For other cases, returns the number of items in values.
                    e.g. ['Q9HD36.A79T', 'Q9ULH7.G370R'] → 2
        """

    soup_single_error = BS(html_text, 'lxml')

    soup_copy = soup_single_error.__copy__()

    for s in soup_copy.select('span'):
        s.extract()

    error_title = get_stripped_error_title(soup_copy.get_text())
    print(' TITLE '.center(40, '-'))
    print('TITLE:', error_title)

    error_items = soup_single_error.find("span", {"class": "resp"})

    print("VALUES:")
    values = [value.strip() for value in error_items.get_text().split(',')]
    print(len(values))
    print(values)

    if error_title == "Duplicates":
        num_values = count_duplicates(values)
    else:
        num_values = len(values)

    return error_title, values, num_values
