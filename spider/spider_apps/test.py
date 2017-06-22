#!/usr/bin/env python
# -*- coding: utf_8 -*-


class TetsFunc(object):
    def test(self, href):
        try:
            _root_url_ = 'https://www.bankersalmanac.com/'
            url = ''
            for con in str(href).split('/'):
                print('con:\t' + con)
                if con == "..":
                    continue
                else:
                    url = url + '/' + con
            return str(_root_url_ + url)
        except Exception as e:
            print(e)