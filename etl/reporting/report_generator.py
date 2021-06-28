import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import base64
import io

ROOT_DIR = os.environ['ROOT_DIR']


class ReportGenerator:

    def __init__(self):
        self.stats = {}
        self.timestamps = None
        self.run_date = ''
        self.crawl_df = None

    def set_stats(self, stats, timestamps, run_date):
        self.stats = stats
        self.timestamps = timestamps
        self.run_date = run_date
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
        template = ''
        with open(os.path.join(ROOT_DIR, 'reporting/report_template.html'), 'r') as template_file:
            template = template_file.read()

        report_header = f"""
        <b>Crawling started: </b> {self.timestamps['crawling_started']}
        <br>
        <b>Crawling ended: </b> {self.timestamps['crawling_ended']}
        <br>
        <b>Enhancement started: </b> {self.timestamps['enhancement_started']}
        <br>
        <b>Enhancement ended: </b> {self.timestamps['enhancement_ended']}
        """

        colors = {'successful': '#22bb33', 'empty': '#f0ad4e', 'failed': '#bb2124',
                  'duplicates': '#aaaaaa', 'missing coordinates': '#5bc0de'}

        template = template.replace('{{DATE}}', self.run_date)
        template = template.replace('{{SUMMARY}}', report_header)
        report_content = ''
        for key in self.stats.keys():
            try:
                total = self.crawl_df[key].sum()
                report_content += '<div class="card">\n'

                crawling_duration = time.strftime('%H:%M:%S', time.gmtime(
                    int(float(self.stats[key].timestamps['crawling_duration']))))
                enhancement_duration = time.strftime('%H:%M:%S', time.gmtime(
                    int(float(self.stats[key].timestamps['enhancement_duration']))))

                css_class = 'crawler-summary' if total > 0 else 'crawler-summary-empty'
                report_content += f"""
                <div class="{css_class}">
                <h3 class="crawler-title">{key}</h3>

                <b>Crawling duration: </b> {crawling_duration}
                <br>
                <b>Enhancement duration: </b> {enhancement_duration}
                <br>
                <b>Crawled entries (total): </b> {total}
                </div>
                """

                if total > 0:
                    plot = self.crawl_df.plot.pie(y=key, figsize=(6, 6), colors=self.crawl_df.index.to_series().apply(
                        lambda x: colors[x]).drop_duplicates(),
                                                  autopct=(lambda p: '{:.0f}'.format(p * total / 100) if p > 0 else ''),
                                                  ylabel='', labels=None)
                    pic_bytes = io.BytesIO()
                    plt.savefig(pic_bytes, format='png')
                    pic_bytes.seek(0)
                    pic_base64 = base64.b64encode(pic_bytes.read())
                    report_content += '<div class="plot"><img src="data:image/png;base64, ' + pic_base64.decode() + '" alt="Plot" /></div>\n'
                report_content += '</div>\n'
            except Exception as e:
                print(key + ": " + str(e))

        template = template.replace('{{REPORT}}', report_content)

        if not os.path.exists(os.path.join(ROOT_DIR, 'reporting/data/')):
            os.makedirs(os.path.join(ROOT_DIR, 'reporting/data/'))
        with open(os.path.join(ROOT_DIR, 'reporting/data/report.html'), 'w') as output:
            output.write(template)
