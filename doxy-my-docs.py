#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import doxymydocs


if __name__ == '__main__':
    config = doxymydocs.AppConfiguration.get_config()

    print(config)


