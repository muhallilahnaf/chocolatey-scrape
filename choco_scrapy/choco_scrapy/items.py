from scrapy import Item, Field
from itemloaders.processors import TakeFirst, Join, MapCompose
import re


# custom processors

def textStrip(text):
    return text.strip()


def removeEmptyString(text):
    return text if text else None


def getFullLink(text):
    return f'https://community.chocolatey.org{text}'


def removeHead(text):
    return text[14:]


def getDLCount(text):
    return ''.join(re.findall(r'\d+', text))


class ChocolateyItem(Item):

    name = Field(
        input_processor=MapCompose(textStrip, removeEmptyString),
        output_processor=TakeFirst()
    )
    link = Field(
        input_processor=MapCompose(textStrip, removeEmptyString, getFullLink),
        output_processor=TakeFirst()
    )
    code = Field(
        input_processor=MapCompose(textStrip, removeEmptyString, removeHead),
        output_processor=TakeFirst()
    )
    downloads = Field(
        input_processor=MapCompose(textStrip, removeEmptyString, getDLCount),
        output_processor=TakeFirst()
    )
