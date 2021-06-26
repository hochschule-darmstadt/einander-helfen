import os
import time
import pandas as pd
import datapane as dp


class ReportGenerator:

    def __init__(self):
        self.stats = {}
        self.timestamps = None
        self.crawl_df = None

    def set_stats(self, stats, timestamps):
        self.stats = stats
        self.timestamps = timestamps
        tmp_dict = {}

        for key in self.stats.keys():
            stats_obj = stats[key]
            tmp_dict[key] = []

            tmp_dict[key].append(stats_obj.crawling_successful - stats_obj.enhancement_duplicates - stats_obj.enhancement_missing_coordinates)
            tmp_dict[key].append(stats_obj.crawling_empty)
            tmp_dict[key].append(len(stats_obj.error_messages['parsing_errors']))
            tmp_dict[key].append(stats_obj.enhancement_duplicates)
            tmp_dict[key].append(stats_obj.enhancement_missing_coordinates)

        self.crawl_df = pd.DataFrame(tmp_dict, index=['successful', 'empty', 'failed', 'duplicates', 'missing coordinates'])

    def build_report(self):
        report_header = f"""<html>
<h1>Crawling summary</h1>

<b>Crawling started: </b> {self.timestamps['crawling_started']}
<br>
<b>Crawling ended: </b> {self.timestamps['crawling_ended']}
<br>
<b>Enhancement started: </b> {self.timestamps['enhancement_started']}
<br>
<b>Enhancement ended: </b> {self.timestamps['enhancement_ended']}
</html>"""

        colors = {'successful': '#22bb33', 'empty': '#f0ad4e', 'failed': '#bb2124',
                  'duplicates': '#aaaaaa', 'missing coordinates': '#5bc0de'}

        blocks = [dp.HTML(report_header)]
        groups = []
        for key in self.stats.keys():
            try:
                total = self.crawl_df[key].sum()
                plot = self.crawl_df.plot.pie(y=key, figsize=(5, 5), colors=self.crawl_df.index.to_series().apply(lambda x: colors[x]).drop_duplicates(), autopct=(lambda p: '{:.0f}'.format(p * total / 100) if p > 0 else ''), ylabel='', labels=None)

                crawling_duration = time.strftime('%H:%M:%S', time.gmtime(int(float(self.stats[key].timestamps['crawling_duration']))))
                enhancement_duration = time.strftime('%H:%M:%S', time.gmtime(int(float(self.stats[key].timestamps['enhancement_duration']))))
                crawler_infos = f"""
<html>
<div style="border: 1px solid black; padding-top: 0px; padding-left: 32px; padding-bottom: 16px">
<h2>{key}</h2>

<b>Crawling duration: </b> {crawling_duration}
<br>
<b>Enhancement duration: </b> {enhancement_duration}
<br>
</div>
</html>
"""
                no_results = f"""
<html>
<div style="border: 1px solid darkred; padding-top: 0px; padding-left: 32px; padding-bottom: 16px">
<h2>{key}</h2>
<i>No results from this crawler.</i>
<br>
</div>
</html>
"""
                if total > 0:
                    inner_group = dp.Group(dp.HTML(crawler_infos), dp.Plot(plot), columns=1)
                else:
                    inner_group = dp.Group(dp.HTML(no_results), columns=1)
                groups.append(inner_group)
            except Exception as e:
                print(key + ": " + str(e))

        blocks.append(dp.Group(blocks=groups, columns=3))

        r = dp.Report(blocks=blocks)
        if not os.path.exists('reporting/data/'):
            os.makedirs('reporting/data/')
        r.save(path='reporting/data/report.html')
