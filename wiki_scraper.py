from bs4 import BeautifulSoup
import requests

def scrape_regions():
    """Get every regions from wikipedia

    Returns:
        region[]: list of regions
    """
    wiki = "https://fr.wikipedia.org/wiki/R%C3%A9gion_fran%C3%A7aise"
    header = {
        'User-Agent': 'Mozilla/5.0'
    }
    page = requests.get(wiki, headers=header)
    soup = BeautifulSoup(page.content)

    tables = soup.findAll("table", {"class": "wikitable"})

    table = tables[2]

    tableau = []
    
    tab = process_table(table)

    # split datas into arrays of string
    for t in tab:
        split = t.split("$", 10)
        to_append = []
        for e in split:
            d = e.strip()
            to_append.append(d)
        tableau.append(to_append)

    # remove first and last element of array
    tableau = tableau[1:-1]
    regions_to_send = []
    count = 0
    # convert array of string into array of region object
    for i, t in enumerate(tableau):

        count = count + 1

        final_result = []
        splitted_deps = t[3].split('(')
        formatted_deps = splitted_deps[1]
        if i == 0:
            formatted_deps = splitted_deps[2]
        chars_to_remove = [",", "et", ")", "ainsi que"]
        for i in chars_to_remove:
            formatted_deps = formatted_deps.replace(i, '')
        final_result = formatted_deps.split(' ')
        final_result[:] = [x for x in final_result if x]
        for i in range(len(final_result)):
            if "--" in final_result[i]:
                final_result[i] = final_result[i].replace("--", "-et-")

        regions = {
            "nom": t[1].split('[')[0],
            "departement": final_result,
            "chef_lieu": t[2].split('[')[0],
            "superficie": int(t[4].replace(u'\xa0', '')),
            "population": int(t[5].replace(u'\xa0', '')),
            "code": int(t[8]),
            "region_id": count
        }
        regions_to_send.append(regions)

    return regions_to_send


def scrape_fromages():
    """Get every cheeses from wikipedia

    Returns:
        fromage[]: list of cheese
    """
    wiki = "https://fr.wikipedia.org/wiki/Liste_des_AOC_et_AOP_laiti%C3%A8res_fran%C3%A7aises"
    header = {
        'User-Agent': 'Mozilla/5.0'
    }
    page = requests.get(wiki, headers=header)
    soup = BeautifulSoup(page.content, features="html.parser")

    tables = soup.findAll("table", {"class": "wikitable"})

    table = tables[0]

    tableau = []

    tab = process_table(table)

    # split datas into array of string
    for t in tab:
        split = t.split("$", 5)
        to_append = []
        for e in split:
            d = e.strip()
            to_append.append(d)
        tableau.append(to_append)

    # remove 1st elem of table
    tableau = tableau[1:]

    fromages_to_send = []
    count = 0
    # convert arary of string into array of fromages
    for t in tableau:

        count = count + 1

        final_result = []

        is_list = False
        for c in t[3]:
            if c == "(":
                is_list = True

        if not is_list:
            d = t[3]
            chars_to_remove = [",", "et", "ainsi que"]
            for i in chars_to_remove:
                d = d.replace(i, '')
            final_result = d.split(' ')
            final_result[:] = [x for x in final_result if x]
            for i in range(len(final_result)):
                if "--" in final_result[i]:
                    final_result[i] = final_result[i].replace("--", "-et-")
        if is_list:
            splitted_deps = t[3].split('(')
            formatted_deps = splitted_deps[1]
            chars_to_remove = [",", "et", ")", "ainsi que"]
            for i in chars_to_remove:
                formatted_deps = formatted_deps.replace(i, '')
            final_result = formatted_deps.split(' ')
            final_result[:] = [x for x in final_result if x]
            for i in range(len(final_result)):
                if "--" in final_result[i]:
                    final_result[i] = final_result[i].replace("--", "-et-")

        fromages = {
            "nom": t[0],
            "departement": final_result,
            "pate": t[2],
            "lait": t[1],
            "annee_aoc": int(t[4]),
            "fromage_id": count
        }
        fromages_to_send.append(fromages)

    return fromages_to_send

def process_table(table):
    # preinit list of lists
    rows = table.findAll("tr")
    row_lengths = [len(r.findAll(['th', 'td'])) for r in rows]
    ncols = max(row_lengths)
    nrows = len(rows)
    data = []
    for i in range(nrows):
        rowD = []
        for j in range(ncols):
            rowD.append('')
        data.append(rowD)

    # process html
    for i in range(len(rows)):
        row = rows[i]
        rowD = []
        cells = row.findAll(["td", "th"])
        for j in range(len(cells)):
            cell = cells[j]

            # lots of cells span cols and rows so lets deal with that
            cspan = int(cell.get('colspan', 1))
            rspan = int(cell.get('rowspan', 1))
            l = 0
            for k in range(rspan):
                # Shifts to the first empty cell of this row
                while data[i + k][j + l]:
                    l += 1
                for m in range(cspan):
                    cell_n = j + l + m
                    row_n = i + k
                    # in some cases the colspan can overflow the table, in those cases just get the last item
                    cell_n = min(cell_n, len(data[row_n]) - 1)
                    data[row_n][cell_n] += cell.text

        data.append(rowD)

    # write data out to tab seperated format
    tab = []
    for i in range(nrows):
        rowStr = '$'.join(data[i])
        tab.append(rowStr)
    return tab
