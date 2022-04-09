import scrapy
from bocconi.items import BocconiItem


class BocconiSpider(scrapy.Spider):
    name = 'bocconi_spider'
    start_urls = [
        'http://didattica.unibocconi.eu/docenti/proff_ord_ruolo.php?dip=53&urlBack=/wps/wcm/connect/Bocconi/SitoPubblico_EN/Navigation+Tree/Home/Faculty+and+Research/Departments/Finance/Faculty/',
        'http://didattica.unibocconi.eu/docenti/proff_ord_ruolo.php?dip=52&urlBack=/wps/wcm/connect/Bocconi/SitoPubblico_EN/Navigation+Tree/Home/Faculty+and+Research/Departments/Ettore+Bocconi+Dep+of+Economics/All+Bocconi+Professors/',
        'http://didattica.unibocconi.eu/docenti/proff_ord_ruolo.php?dip=51&urlBack=/wps/wcm/connect/Bocconi/SitoPubblico_EN/Navigation+Tree/Home/Faculty+and+Research/Departments/Accounting/Faculty/',
        'http://didattica.unibocconi.eu/docenti/proff_ord_ruolo.php?dip=55&urlBack=/wps/wcm/connect/Bocconi/SitoPubblico_EN/Navigation+Tree/Home/Faculty+and+Research/Departments/Decision+Sciences/Faculty/',
    ]

    def parse(self, response):
        faculty_list = response.xpath("//div[@class='txtParagrafo']/div/a/@href").extract()
        faculty_list = [i for i in faculty_list if 'ancor' not in i]
        print('the number of faculties is......' + str(len(faculty_list)))
        for faculty in faculty_list:
            yield response.follow(faculty, callback=self.parse_detail)

    def parse_detail(self, response):
        item = BocconiItem()
        item['name'] = response.xpath("//h1/text()").extract_first().title()
        temp = response.xpath("//div[@class='txtParagrafo']//div/text()").extract()
        temp = [i.strip() for i in temp]
        temp = [i for i in temp if i]
        item['title'] = temp[0]
        item['email'] = response.xpath("//a[contains(@title, 'Email')]/text()").extract_first()
        s = response.xpath("//h2[contains(text(), 'Biographical note')]/following-sibling:: div[1]/p//text()").extract()
        if s:
            s = [i.strip() for i in s]
            s = [i for i in s if i]
            item['bio_note'] = ' '.join(s)
        else:
            item['bio_note'] = None
        cv = response.xpath("//h2[contains(text(), 'Academic CV')]/following-sibling:: div[1]/p//text()").extract()
        if cv:
           cv = [i.strip() for i in cv]
           cv = [i for i in cv if i]
           item['academic_cv'] = ' '.join(cv)
        else:
           item['academic_cv'] = None
        research = response.xpath("//h2[contains(text(), 'Research areas')]/following-sibling:: div[1]/p//text()").extract()
        if research:
            research = [i.strip() for i in research]
            research = [i for i in research if i]
            item['research_area'] = ' '.join(research)
        else:
            item['research_area'] = None
        courses = response.xpath("//h2[contains(text(), 'Courses a.y. 2017/2018')]/following-sibling:: div[1]//text()").extract()
        courses = [i.strip() for i in courses]
        courses = [i for i in courses if i]
        courses = [(courses[i] + ' ' + courses[i+1]) for i in range(0, len(courses), 2)]
        courses = [course.title() for course in courses]
        item['course'] = courses
        pubs = response.xpath("//h2[contains(text(), 'Selected publications')]/following-sibling:: div[1]//text()").extract()[:6]
        item['pubs'] = pubs
        item['personal_page'] = response.xpath("//a[contains(text(), 'Personal page')]/@href").extract_first()

        yield item