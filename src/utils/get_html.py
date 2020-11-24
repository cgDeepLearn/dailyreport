#!/usr/bin/python
# coding:utf8


class GetHtml(object):
    def __init__(self):
        self._html_head = "<html><body>"
        self._format_html_foot = """<p style="font-family: verdana,arial,sans-serif;font-size:10px;font-weight:lighter;">%s</p>"""
        self._format_html_head = """<p style="font-family: verdana,arial,sans-serif;font-size:12px;font-weight:bold;">%s</p>"""
        self._format_html_img = """<br><img src="cid:%s" alt="" width="1200" height="600"></br>"""
        self._html_tail = "</body></html>"
        self._html_p_head = """<p style="font-family: verdana,arial,sans-serif;font-size:12px;font-weight:bold;">%s</p>"""

        self._table_head = """<table style="font-family: verdana,arial,sans-serif;font-size:11px;color:#333333;border-width: 1px;border-color: #666666;border-collapse: collapse;" border="1"><tr>"""
        self._format_table_th = """<th style="border-width: 1px;padding: 8px;border-style: solid;border-color: #666666;background-color: #dedede;" nowrap>%s</th>"""

        self._format_table_td = """<td style="border-width: 1px;padding: 8px;text-align: right;border-style: solid;border-color: #666666;background-color: #ffffff;" align="right" nowrap>%s</td>"""
        self._table_tail = "</table>"
        self._content = ""

        self._table_html = []

    def add_table(self, table_title, th_info, td_info_list):
        table_str = ""
        table_p_head = self._html_p_head % (str(table_title))
        table_str = table_p_head + self._table_head
        # th
        table_str += "<tr>"
        for th in th_info:
            temp_str = self._format_table_th % (str(th))
            table_str += temp_str
        table_str += "</tr>"
        # td
        for td_info in td_info_list:
            table_str += "<tr>"
            for td in td_info:
                temp_str = self._format_table_td % (str(td))
                table_str += temp_str
            table_str += "</tr>"
        #
        table_str += self._table_tail
        self._table_html.append(table_str)

    def add_head(self, head):
        head_str = self._format_html_head % (str(head))
        self._table_html.append(head_str)

    def add_foot(self, foot):
        foot_str = self._format_html_foot % (str(foot))
        self._table_html.append(foot_str)
    
    def add_img(self, img):
        img_str = self._format_html_img % (str(img))
        self._table_html.append(img_str)

    def output_html(self):
        html_content = self._html_head
        for s in self._table_html:
            html_content += s
        html_content += self._html_tail
        return html_content


if __name__ == "__main__":
    gh = GetHtml()
    p_title = "test"
    th = [1, 2, 3, 4]
    td = [[1, 2, 3, 4], [4, 5, 5, 56], [3, 3, 3, 3]]
    gh.add_table(p_title, th, td)
    cont = gh.output_html()
    import src.utils.sendmail
    src.utils.sendmail.send_mail(['edgar.chen@xiaoying.com'], 'test', cont)
