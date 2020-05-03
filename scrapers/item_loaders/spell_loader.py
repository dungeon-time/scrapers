import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity
from scrapers.items.spell import Spell

process_alternate_components = lambda v: re.findall('^\*\s\-\s\((.*)\)', v)[0] #remove '* -(' from the beginning, and ')' from the end
process_components = lambda v: re.sub('\s\*$', '', v).split(',') #remove ' *' from the end
process_source_book_page = lambda v: re.sub('^\,\spg\.\s', '', v) #remove ', pg. ' from the beginning
process_spell_aoe_size = lambda v: re.findall('^.*\((\d+\sft)', v)[0] #extract the spell distance '<span class=\"aoe-size\">(30 ft <i class=\"i-aoe-line\"></i>)</span>' => 30 ft
process_spell_attack_save = lambda v: re.sub('\sSave', '', v) #remove ' Save' from the end
process_spell_damage_effect = lambda v: re.sub('\(\.{3}\)', '', v) #remove '(...) from the end
process_spell_shape = lambda v: re.findall('^.*i\-aoe-(.*)\"', v)[0] #extract the end of the icon class '<span class=\"aoe-size\">(30 ft <i class=\"i-aoe-line\"></i>)</span>' => line

class SpellLoader(ItemLoader):

    default_item_class = Spell
    default_output_processor = TakeFirst()

    name_in = MapCompose(unicode.strip)
    level_in = MapCompose(unicode.strip)
    school_in = MapCompose(unicode.strip)
    components_in = MapCompose(process_components, unicode.strip)
    components_out = Identity()
    cast_time_in = MapCompose(unicode.strip)
    duration_in = MapCompose(unicode.strip)
    spell_range_in = MapCompose(unicode.strip)
    spell_aoe_size_in = MapCompose(process_spell_aoe_size, unicode.strip)
    spell_shape_in = MapCompose(process_spell_shape, unicode.strip, unicode.title)
    spell_attack_save_in = MapCompose(process_spell_attack_save, unicode.strip)
    spell_damage_effect_in = MapCompose(process_spell_damage_effect, unicode.strip)
    description_in = MapCompose(unicode.strip)
    tags_in = MapCompose(unicode.strip)
    tags_out = Identity()
    classes_in = MapCompose(unicode.strip)
    classes_out = Identity()
    source_book_in = MapCompose(unicode.strip)
    source_book_page_in = MapCompose(process_source_book_page, unicode.strip)
    alternate_components_in = MapCompose(process_alternate_components, unicode.strip)