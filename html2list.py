import xml.etree.ElementTree as et


def html2list(table):
    if isinstance(table, str):
        table = et.fromstring(table)

    # parse caption
    caption = table.find("caption")
    caption = caption.text if caption is not None else ''

    # parse table
    content = []
    rowspans = {}
    contents = {}

    for elem in table.iter(tag="tr"):
        row = []
        cell_index = 0

        for cell in list(elem):
            cell_text = ''.join(cell.itertext()).strip()

            rowspan = cell.get("rowspan")
            rowspans[cell_index] = int(rowspan) if rowspan else (rowspans.get(cell_index, 0))
            if rowspan is not None:
                contents[cell_index] = cell_text

            if rowspan is None and rowspans[cell_index] > 0:
                row.append(contents[cell_index])
                rowspans[cell_index] -= 1

            colspan = cell.get("colspan")
            colspan = int(colspan) if colspan else 1
            row.extend([''.join(cell_text)] * colspan)

            cell_index += colspan
        content.append(row)

    return caption, content


def repr_table(caption, content):
    rpr = []
    max_widths = []
    for row in content:
        col_widths = list(map(lambda t: len(max(t, key=len)), zip(*content)))
        max_widths.append(sum(col_widths) + 2*len(col_widths))
        rpr.append("  ".join("{:<{r}}".format(cell, r=align) for cell, align in zip(row, col_widths)))

    return "{:^{c}}\n\n{}".format(caption, "\n".join(rpr), c=max(max_widths))
