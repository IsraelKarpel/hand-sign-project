import re
from xml.dom import minidom

def SuffixOfPoseByLanguage(language):
    if language == "zh": #Chinese
        return "zh.zh"
    if language == "da": #Danish
        return "da.da"
    if language == "nl": #Dutch
        return "nl.nl"
    if language == "en": #English
        return "en.us"
    if language == "fr": #French
        return "fr.fr"
    if language == "de": #German
        return "de.de"
    if language == "el": #Greek
        return "el.el"
    if language == "it": #Italian
        return "it.it"
    if language == "ja": #Japanese
        return "ja.ja"
    if language == "lt": #Lithuanian
        return "lt.lt"
    if language == "nb": #Norwegian
        return "nb.nb"
    if language == "pl": #Polish
        return "pl.pl"
    if language == "pt": #Portuguese
        return "pt.pt"
    if language == "ro": #Romanian
        return "ro.ro"
    if language == "re": #Russian
        return "re.re"
    if language == "es": #Spanish
        return "es.es"




def getLanguge(ttml_dom):
    tt_element = ttml_dom.getElementsByTagName('tt')[0]
    language_tag = tt_element.getAttribute('xml:lang')
    lang = re.split(r'\s+', language_tag.strip())[0].split('-')[0]
    return lang


def getCaptions(tt_element):
    array_lines = [i for i in tt_element.getElementsByTagName('p') \
                   if 'begin' in i.attributes.keys()]
    return array_lines


def extract_dialogue(nodes, styles=None):
    """Extract text content and styling attributes from <p> elements.
        Args:
            nodes (xml.dom.minidom.Node): List of <p> elements
            styles (list): List of style signifiers that should be
                applied to each node
        Return:
            List of SRT paragraphs (strings)
        """

    if styles is None:
        styles = []
    dialogue = []

    for node in nodes:

        _styles = []

        if node.nodeType == node.TEXT_NODE:

            format_str = '{}'

            # Take the liberty to make a few stylistic choices. We don't
            # want too many leading spaces or any unnessary new lines
            text = re.sub(r'^\s{4,}', '', node.nodeValue.replace('\n', ''))

            for style in styles:
                format_str = '{ot}{f}{et}'.format(
                    et='</{}>'.format(style),
                    ot='<{}>'.format(style),
                    f=format_str)

            try:
                dialogue.append(format_str.format(text))
            except UnicodeEncodeError:
                dialogue.append(format_str.format(text.encode('utf8')))

        elif node.localName == 'br':
            dialogue.append('\n')

        # Checks for italics for now but shouldn't be too much work to
        # support bold text or colors
       # elif node.localName == 'span':
        #    style_attrs = self.get_tt_style_attrs(node)
         #   inline_italic = style_attrs['font_style'] == 'italic'
          #  assoc_italic = style_attrs['style_id'] in self.italic_style_ids
           # if inline_italic or assoc_italic:
            #    _styles.append('i')

        if node.hasChildNodes():
            dialogue += extract_dialogue(node.childNodes, _styles)

    return ''.join(dialogue)


def get_tt_style_attrs(self, node, in_head=False):
    """Extract node's style attributes
    Node can be a style definition element or a content element (<p>).
    Attributes are filtered against :attr:`Ttml2Srt.allowed_style_attrs`
    and returned as a dict whose keys are attribute names camel cased.
    """

    style = {}
    for attr_name in self.allowed_style_attrs:
        tts = 'tts:' + attr_name
       # attr_name = Ttml2Srt.snake_to_camel(attr_name)
        style[attr_name] = node.getAttribute(tts) or ''
    if not in_head:
        style['style_id'] = node.getAttribute('style')
    return style


def process_parag(paragraph):
    """Extract begin and end attrs, and text content of <p> element.
    Args:
        paragragh (xml.dom.minidom.Element): <p> element.
    Returns:
        Tuple containing
            begin in ms,
            end in ms,
            begin in subrip form,
            end in subrip form,
            text content in Subrip (SRT) format.
    """

    begin = paragraph.attributes['begin'].value
    end = paragraph.attributes['end'].value

    begin2 = str(begin).strip('s')
    end2 = str(end).strip('s')

    duration = float(end2) - float(begin2)

    dialogue = extract_dialogue(paragraph.childNodes)

    #return ms_begin, ms_end, #subrip_begin,# subrip_end, dialogue
    return duration, dialogue




def getArrfromCaptions(subsfilepath):
    ttml_dom = minidom.parse(subsfilepath)
    # get the language of the subtitle
    language = getLanguge(ttml_dom)
    # get the matche suffix fro the curret language
    suffix = SuffixOfPoseByLanguage(language)
    # get all of the information from the subtitle
    lines_of_information = getCaptions(ttml_dom)
    subs = []  # subs will contains two element every line, the first is the duraiton of that line
    # and the second is the text of the subtitle line
    for line in lines_of_information:
        duration, dialogue = process_parag(line)
        subs.append((duration, dialogue))
    return subs,suffix,language
