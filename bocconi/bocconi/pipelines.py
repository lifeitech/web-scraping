# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.contrib.exporter import CsvItemExporter


class BocconiPipeline2(object):

    def open_spider(self, spider):
        self.file = open('output.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class BocconiPipeline(object):

    def open_spider(self, spider):
        self.file = open('/Users/francis/Desktop/output.txt', 'w')

    def process_item(self, item, spider):
        self.file.write('\\rule{\\textwidth}{1pt}\n')
        self.file.write('{{\\large\\href{{{0}}}{{{1}}}}} ~ {2}\\\\\n'.format(item['personal_page'], item['name'], item['title']))
        self.file.write('{0}\\\\'.format(item['email']))
        self.file.write('\n\n')
        self.file.write('\\textbf{{Research Area}}\\\\\n')
        self.file.write('{0}\\\\'.format(item['research_area']))
        self.file.write('\n\n')
        self.file.write('\\textbf{{Biographical Note}}\\\\\n')
        self.file.write('{0}\\\\'.format(item['bio_note']))
        self.file.write('\n\n')
        self.file.write('\\textbf{{Courses a.y. 2017/2018}}\n')
        self.file.write('\\bi\n')
        for i in range(len(item['course'])):
            self.file.write('\\item {0}\n'.format(item['course'][i]))
        self.file.write('\\ei')
        self.file.write('\n\n')
        return item

    def close_spider(self, spider):
        self.file.close()