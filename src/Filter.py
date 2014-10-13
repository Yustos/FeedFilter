# -*- coding: utf-8 *-*
import feedparser
import urllib2
import datetime
from dateutil.parser import parse
import PyRSS2Gen
import Cache
from bs4 import BeautifulSoup
from tornado import log

class Processor():
    def __init__(self, blackList):
        self._cache = Cache.Cache()
        self._blackList = set(l.lower() for l in blackList)

    def Parse(self, url):
        proxy = urllib2.ProxyHandler( {} )
        feed = feedparser.parse(url, handlers = [proxy])
        if feed["bozo"]:
            if "summary" in feed["feed"]:
                log.app_log.error(feed["feed"]["summary"])
            if "bozo_exception" in feed:
                log.app_log.error("Bozo ex: %s" % feed["bozo_exception"])
            return
        entries = []
        for entry in feed.entries:
            articleUrl = entry.links[0].href
            cache = self._cache.check(articleUrl)
            if not cache["Cached"]:
                tags = self.AcquireTags(articleUrl)
                cache["Blocked"] = not self._blackList.isdisjoint(tags)
                self._cache.add(articleUrl, tags, cache["Blocked"])
            if not cache["Blocked"]:
                entries.append(entry)
        return self.MapFeed(feed, entries)

    def AcquireTags(self, articleUrl):
        proxy = urllib2.ProxyHandler( {} )
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        html = urllib2.urlopen(articleUrl)
        soup = BeautifulSoup(html)
        tagContainer = soup.find("span", "story_tag_list")
        tags = [x.text.lower() for x in tagContainer.find_all("span")]
        return tags

    def MapFeed(self, feed, entries):
        items = []
        for entry in entries:
            items.append(self.MapEntry(entry))

        rss = PyRSS2Gen.RSS2(
            title=feed.feed.title,
            link=feed['href'],
            description="Reprocessed feed",
            lastBuildDate=datetime.datetime.now(),
            items=items)
        xml = rss.to_xml(encoding = "utf-8")
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