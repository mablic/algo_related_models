#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


def get_sp():

    df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    all_companies = df[0][0].tolist()
    return all_companies


if __name__ == '__main__':
    print(get_sp())
