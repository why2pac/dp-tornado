# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller
from bs4 import BeautifulSoup


class PaginationController(Controller):
    def get(self):
        self.test_simple_1()
        self.test_simple_2()
        self.test_all()
        self.test_first_page()
        self.test_last_page()
        self.test_first_block()
        self.test_last_block()
        self.test_render()

    def test_render(self):
        params = {
            'total_count': 100,
            'page': 3,
            'rpp': 10,
            'kwargs': {

            }
        }

        self.render('tests/view/module/pagination.html', params)

    def test_simple_1(self):
        params = {
            'total_count': 100,
            'page': 3,
            'rpp': 10,
            'kwargs': {

            }
        }

        pagination = self.render_string('tests/view/module/pagination.html', params)
        pagination = BeautifulSoup(pagination, 'lxml')

        assert(len(pagination.findAll('div')) == 1)
        assert(len(pagination.find('div').findAll('strong')) == 1)
        assert(len(pagination.find('div').findAll('a')) == 9)

    def test_simple_2(self):
        params = {
            'total_count': 1000,
            'page': 25,
            'rpp': 10,
            'kwargs': {

            }
        }

        pagination = self.render_string('tests/view/module/pagination.html', params)
        pagination = BeautifulSoup(pagination, 'lxml')

        assert(len(pagination.findAll('div')) == 1)
        assert(len(pagination.find('div').findAll('strong')) == 1)
        assert(len(pagination.find('div').findAll('a')) == 13)

    def test_all(self):
        region_tag = 'div'
        region_class = 'region-class'

        first = 'First'
        first_class = 'first-class'

        last = 'Last'
        last_class = 'last-class'

        prev_block = 'Prev-Block'
        prev_block_class = 'prev-block-class'

        next_block = 'Next-Block'
        next_block_class = 'next-block-class'

        prev = 'Prev'
        prev_class = 'prev-class'

        next = 'Next'
        next_class = 'next-class'

        current_tag = 'strong'
        current_class = 'current-class'

        link_tag = 'a'
        link_class = 'link-class'

        params = {
            'total_count': 10000,
            'page': 33,
            'rpp': 10,
            'kwargs': {
                'region_tag': region_tag,
                'region_class': region_class,

                'first': first,
                'first_class': first_class,

                'last': last,
                'last_class': last_class,

                'prev_block': prev_block,
                'prev_block_class': prev_block_class,

                'next_block': next_block,
                'next_block_class': next_block_class,

                'prev': prev,
                'prev_class': prev_class,

                'next': next,
                'next_class': next_class,

                'current_tag': current_tag,
                'current_class': current_class,

                'link_tag': link_tag,
                'link_class': link_class,

                'space': '_'
            }
        }

        pagination = self.render_string('tests/view/module/pagination.html', params)
        pagination = BeautifulSoup(pagination, 'lxml')

        assert(len(pagination.findAll(region_tag)) == 1)
        assert(pagination.find(region_tag).attrs['class'][0] == region_class)
        assert(len(pagination.find(region_tag).findAll(link_tag)) == 15)

        links = pagination.find(region_tag).findAll(link_tag)

        assert(links[0].attrs['class'][0] == first_class)
        assert(links[0].text == first)

        assert(links[1].attrs['class'][0] == prev_block_class)
        assert(links[1].text == prev_block)

        assert(links[2].attrs['class'][0] == prev_class)
        assert(links[2].text == prev)

        assert(links[-3].attrs['class'][0] == next_class)
        assert(links[-3].text == next)

        assert(links[-2].attrs['class'][0] == next_block_class)
        assert(links[-2].text == next_block)

        assert(links[-1].attrs['class'][0] == last_class)
        assert(links[-1].text == last)

        links = links[3:-3]

        for e in links:
            assert(e.name == link_tag)
            assert(e.attrs['class'][0] == link_class)
            assert(self.helper.numeric.extract_numbers(e.text) == e.text)

    def test_first_page(self):
        region_tag = 'div'
        region_class = 'region-class'

        first = 'First'
        first_class = 'first-class'

        last = 'Last'
        last_class = 'last-class'

        prev_block = 'Prev-Block'
        prev_block_class = 'prev-block-class'

        next_block = 'Next-Block'
        next_block_class = 'next-block-class'

        prev = 'Prev'
        prev_class = 'prev-class'

        next = 'Next'
        next_class = 'next-class'

        current_tag = 'strong'
        current_class = 'current-class'

        link_tag = 'a'
        link_class = 'link-class'

        params = {
            'total_count': 10000,
            'page': 1,
            'rpp': 10,
            'kwargs': {
                'region_tag': region_tag,
                'region_class': region_class,

                'first': first,
                'first_class': first_class,

                'last': last,
                'last_class': last_class,

                'prev_block': prev_block,
                'prev_block_class': prev_block_class,

                'next_block': next_block,
                'next_block_class': next_block_class,

                'prev': prev,
                'prev_class': prev_class,

                'next': next,
                'next_class': next_class,

                'current_tag': current_tag,
                'current_class': current_class,

                'link_tag': link_tag,
                'link_class': link_class,

                'space': '_'
            }
        }

        pagination = self.render_string('tests/view/module/pagination.html', params)
        pagination = BeautifulSoup(pagination, 'lxml')

        assert(len(pagination.findAll(region_tag)) == 1)
        assert(pagination.find(region_tag).attrs['class'][0] == region_class)
        assert(len(pagination.find(region_tag).findAll(link_tag)) == (15 - 3))

        links = pagination.find(region_tag).findAll(link_tag)

        assert(links[-3].attrs['class'][0] == next_class)
        assert(links[-3].text == next)

        assert(links[-2].attrs['class'][0] == next_block_class)
        assert(links[-2].text == next_block)

        assert(links[-1].attrs['class'][0] == last_class)
        assert(links[-1].text == last)

        links = links[0:-3]

        for e in links:
            assert(e.name == link_tag)
            assert(e.attrs['class'][0] == link_class)
            assert(self.helper.numeric.extract_numbers(e.text) == e.text)

    def test_last_page(self):
        region_tag = 'div'
        region_class = 'region-class'

        first = 'First'
        first_class = 'first-class'

        last = 'Last'
        last_class = 'last-class'

        prev_block = 'Prev-Block'
        prev_block_class = 'prev-block-class'

        next_block = 'Next-Block'
        next_block_class = 'next-block-class'

        prev = 'Prev'
        prev_class = 'prev-class'

        next = 'Next'
        next_class = 'next-class'

        current_tag = 'strong'
        current_class = 'current-class'

        link_tag = 'a'
        link_class = 'link-class'

        params = {
            'total_count': 10000,
            'page': 1000,
            'rpp': 10,
            'kwargs': {
                'region_tag': region_tag,
                'region_class': region_class,

                'first': first,
                'first_class': first_class,

                'last': last,
                'last_class': last_class,

                'prev_block': prev_block,
                'prev_block_class': prev_block_class,

                'next_block': next_block,
                'next_block_class': next_block_class,

                'prev': prev,
                'prev_class': prev_class,

                'next': next,
                'next_class': next_class,

                'current_tag': current_tag,
                'current_class': current_class,

                'link_tag': link_tag,
                'link_class': link_class,

                'space': '_'
            }
        }

        pagination = self.render_string('tests/view/module/pagination.html', params)
        pagination = BeautifulSoup(pagination, 'lxml')

        assert(len(pagination.findAll(region_tag)) == 1)
        assert(pagination.find(region_tag).attrs['class'][0] == region_class)
        assert(len(pagination.find(region_tag).findAll(link_tag)) == (15 - 3))

        links = pagination.find(region_tag).findAll(link_tag)

        assert(links[0].attrs['class'][0] == first_class)
        assert(links[0].text == first)

        assert(links[1].attrs['class'][0] == prev_block_class)
        assert(links[1].text == prev_block)

        assert(links[2].attrs['class'][0] == prev_class)
        assert(links[2].text == prev)

        links = links[3:]

        for e in links:
            assert(e.name == link_tag)
            assert(e.attrs['class'][0] == link_class)
            assert(self.helper.numeric.extract_numbers(e.text) == e.text)

    def test_first_block(self):
        region_tag = 'div'
        region_class = 'region-class'

        first = 'First'
        first_class = 'first-class'

        last = 'Last'
        last_class = 'last-class'

        prev_block = 'Prev-Block'
        prev_block_class = 'prev-block-class'

        next_block = 'Next-Block'
        next_block_class = 'next-block-class'

        prev = 'Prev'
        prev_class = 'prev-class'

        next = 'Next'
        next_class = 'next-class'

        current_tag = 'strong'
        current_class = 'current-class'

        link_tag = 'a'
        link_class = 'link-class'

        params = {
            'total_count': 10000,
            'page': 2,
            'rpp': 10,
            'kwargs': {
                'region_tag': region_tag,
                'region_class': region_class,

                'first': first,
                'first_class': first_class,

                'last': last,
                'last_class': last_class,

                'prev_block': prev_block,
                'prev_block_class': prev_block_class,

                'next_block': next_block,
                'next_block_class': next_block_class,

                'prev': prev,
                'prev_class': prev_class,

                'next': next,
                'next_class': next_class,

                'current_tag': current_tag,
                'current_class': current_class,

                'link_tag': link_tag,
                'link_class': link_class,

                'space': '_'
            }
        }

        pagination = self.render_string('tests/view/module/pagination.html', params)
        pagination = BeautifulSoup(pagination, 'lxml')

        assert(len(pagination.findAll(region_tag)) == 1)
        assert(pagination.find(region_tag).attrs['class'][0] == region_class)
        assert(len(pagination.find(region_tag).findAll(link_tag)) == (15 - 2))

        links = pagination.find(region_tag).findAll(link_tag)

        assert(links[0].attrs['class'][0] == prev_class)
        assert(links[0].text == prev)

        assert(links[-3].attrs['class'][0] == next_class)
        assert(links[-3].text == next)

        assert(links[-2].attrs['class'][0] == next_block_class)
        assert(links[-2].text == next_block)

        assert(links[-1].attrs['class'][0] == last_class)
        assert(links[-1].text == last)

        links = links[1:-3]

        for e in links:
            assert(e.name == link_tag)
            assert(e.attrs['class'][0] == link_class)
            assert(self.helper.numeric.extract_numbers(e.text) == e.text)

    def test_last_block(self):
        region_tag = 'div'
        region_class = 'region-class'

        first = 'First'
        first_class = 'first-class'

        last = 'Last'
        last_class = 'last-class'

        prev_block = 'Prev-Block'
        prev_block_class = 'prev-block-class'

        next_block = 'Next-Block'
        next_block_class = 'next-block-class'

        prev = 'Prev'
        prev_class = 'prev-class'

        next = 'Next'
        next_class = 'next-class'

        current_tag = 'strong'
        current_class = 'current-class'

        link_tag = 'a'
        link_class = 'link-class'

        params = {
            'total_count': 10000,
            'page': 999,
            'rpp': 10,
            'kwargs': {
                'region_tag': region_tag,
                'region_class': region_class,

                'first': first,
                'first_class': first_class,

                'last': last,
                'last_class': last_class,

                'prev_block': prev_block,
                'prev_block_class': prev_block_class,

                'next_block': next_block,
                'next_block_class': next_block_class,

                'prev': prev,
                'prev_class': prev_class,

                'next': next,
                'next_class': next_class,

                'current_tag': current_tag,
                'current_class': current_class,

                'link_tag': link_tag,
                'link_class': link_class,

                'space': '_'
            }
        }

        pagination = self.render_string('tests/view/module/pagination.html', params)
        pagination = BeautifulSoup(pagination, 'lxml')

        assert(len(pagination.findAll(region_tag)) == 1)
        assert(pagination.find(region_tag).attrs['class'][0] == region_class)
        assert(len(pagination.find(region_tag).findAll(link_tag)) == (15 - 2))

        links = pagination.find(region_tag).findAll(link_tag)

        assert(links[0].attrs['class'][0] == first_class)
        assert(links[0].text == first)

        assert(links[1].attrs['class'][0] == prev_block_class)
        assert(links[1].text == prev_block)

        assert(links[2].attrs['class'][0] == prev_class)
        assert(links[2].text == prev)

        assert(links[-1].attrs['class'][0] == next_class)
        assert(links[-1].text == next)

        links = links[3:-1]

        for e in links:
            assert(e.name == link_tag)
            assert(e.attrs['class'][0] == link_class)
            assert(self.helper.numeric.extract_numbers(e.text) == e.text)
