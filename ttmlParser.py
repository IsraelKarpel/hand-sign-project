import re


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
