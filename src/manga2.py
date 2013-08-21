import argparse
import itertools

from redux.helper.util import Util
from redux.site.mangafox import MangaFox
from redux.site.mangahere import MangaHere
from redux.site.mangapanda import MangaPanda
from redux.site.mangareader import MangaReader


def main():
    parser = argparse.ArgumentParser(description='Download manga.')
    subparsers = parser.add_subparsers()
    add_list_subparser(subparsers)
    add_download_subparser(subparsers)

    args = parser.parse_args()
    args.func(args)


def add_list_subparser(subparsers):
    parser = subparsers.add_parser('list', help='list all chapters')
    parser.add_argument('series', help='series name')
    parser.set_defaults(func=itemize)


def add_download_subparser(subparsers):
    parser = subparsers.add_parser('download', help='download some chapters')
    parser.add_argument('series', help='series name')
    parser.add_argument('chapters', help='a quoted string of comma delimited numbers or ranges')
    parser.set_defaults(func=download)


def chapters(series):
    chapters = Util.flatten([
        site.series(series).chapters for site in [MangaFox, MangaHere, MangaPanda, MangaReader]
    ])

    return itertools.groupby(
        Util.natural_sort(chapters, key=lambda chapter: chapter.chapter),
        lambda chapter: chapter.chapter
    )


def itemize(args):
    for chapter_number, chapter_objects in chapters(args.series):
        titles = [chapter.title for chapter in chapter_objects if chapter.title.strip() != '']
        print "(%s) %s" % (chapter_number, titles[0] if len(titles) > 0 else '')


def download(args):
    return


if __name__ == '__main__':
    main()