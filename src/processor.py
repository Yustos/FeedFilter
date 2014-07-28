# -*- coding: utf-8 *-*
import feedparser
import urllib2
import datetime
from dateutil.parser import parse
import PyRSS2Gen
import cache
from bs4 import BeautifulSoup


class Processor():
    def __init__(self):
        self._cache = cache.Cache()

    def Parse(self, url):
        feed = feedparser.parse(url)
        for entry in feed.entries:
            articleUrl = entry.links[0].href
            if self._cache.check(articleUrl):
                print("already in cache: %s" % articleUrl)
            else:
                tags = self.AcquireTags(entry)
                self._cache.add(articleUrl, tags)
        return self.MapFeed(feed)

    def AcquireTags(self, articleUrl, entry):
        html = urllib2.urlopen(articleUrl)
        soup = BeautifulSoup(html)
        tagContainer = soup.find("span", "story_tag_list")
        tags = [x.text for x in tagContainer.find_all("span")]
        return tags

    def MapFeed(self, feed):
        items = []
        for entry in feed.entries:
            items.append(self.MapEntry(entry))

        rss = PyRSS2Gen.RSS2(
            title=feed.feed.title,
            link="http://example.com/rss",
            description="Reprocessed feed",
            lastBuildDate=datetime.datetime.now(),
            items=items)
        #rss.write_xml(open("out1.xml", "w"))
        xml = rss.to_xml()
        return xml

    def MapEntry(self, entry):
        reflink = entry.links[0].href
        item = PyRSS2Gen.RSSItem(
            title=entry.title,
            link=reflink,
            description=entry.description,
            guid=PyRSS2Gen.Guid(reflink),
            pubDate=parse(entry.published))
        return item