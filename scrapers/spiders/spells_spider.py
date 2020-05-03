import scrapy
from scrapy.loader import ItemLoader
from scrapers.item_loaders.spell_loader import SpellLoader

class QuotesSpider(scrapy.Spider):
  name = "spells"
  allowed_domains = ['www.dndbeyond.com']
  start_urls = ['https://www.dndbeyond.com/spells']

  def parse(self, response):
    next_page = response.xpath('//a[@data-next-page]/@href').get()

    if next_page is not None:
      next_page_url = response.urljoin(next_page)
      yield response.follow(next_page_url, callback=self.parse)

    for slug in response.xpath('//div[@data-type="spells"]/@data-slug').getall():
      details_page_url = response.urljoin('/spells/' + slug)
      yield response.follow(details_page_url, callback=self.get_spell_details)

  def get_spell_details(self, response):
    loader = SpellLoader(selector=response)

    loader.add_css('name', 'h1.page-title::text')
    loader.add_css('level', '.ddb-statblock-item-level .ddb-statblock-item-value::text')
    loader.add_css('school', '.ddb-statblock-item-school .ddb-statblock-item-value::text')
    loader.add_css('components', '.ddb-statblock-item-components .component-asterisks::text')
    loader.add_css('cast_time', '.ddb-statblock-item-casting-time .ddb-statblock-item-value::text')
    loader.add_css('duration', '.ddb-statblock-item-duration .ddb-statblock-item-value::text')
    loader.add_css('spell_range', '.ddb-statblock-item-range-area .ddb-statblock-item-value::text')
    loader.add_css('spell_aoe_size', '.ddb-statblock-item-range-area .ddb-statblock-item-value .aoe-size')
    loader.add_css('spell_shape', '.ddb-statblock-item-range-area .ddb-statblock-item-value .aoe-size')
    loader.add_css('spell_attack_save', '.ddb-statblock-item-attack-save .ddb-statblock-item-value span::text')
    loader.add_css('spell_damage_effect', '.ddb-statblock-item-damage-effect .ddb-statblock-item-value::text')
    loader.add_css('description', '.more-info-content p::text')
    loader.add_css('tags', '.spell-tag::text')
    loader.add_css('classes', '.class-tag::text')
    loader.add_css('source_book', '.spell-source::text')
    loader.add_css('source_book_page', '.page-number::text')
    loader.add_css('alternate_components', '.components-blurb::text')

    return loader.load_item()

    # TODO: use all .css, convert .xpath
    # TODO: missing 1 spell? 514 instead of 515
    # TODO: write next_page(_url) to a file to see where the bad entries are coming from
    # TODO: additional tables: spell_damage_effect, school, tags, source_book, level, attribute (STR, CON, etc.), classes, subclasses, components, cast_time, cast_target