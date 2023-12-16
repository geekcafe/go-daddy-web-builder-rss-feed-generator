"""
Html Creater
"""
class HtmlCreator:
    """
    HtmlCreator Class
    """

    @staticmethod
    def create_html_from_json_content(json_data):
        """
        Creates html from json content string
        """
        html_blocks = []
        if "blocks" in json_data:
            blocks = json_data["blocks"]
            for block in blocks:
                html = HtmlCreator.get_content_from_block(block)
                if html:
                    html_blocks.append(html)
                # print(html)

                # print(block)
                

        return "\n".join(html_blocks)
    
    @staticmethod
    def get_content_from_block(block: dict):
        """
        Gets content / value from a block
        """
        text = block.get("text")
        html = None
        if text:
            style = HtmlCreator.get_style_from_block(block)
            html = f"<p><span style=\"{style}\">{text}</span></p>"
            

        return html

    @staticmethod
    def get_style_from_block(block: dict):
        """
        Gets the style information from a block
        """
        styles = []

        if "inlineStyleRanges" in block:
            for style in block["inlineStyleRanges"]:
                if str(style["style"]).lower() == 'bold':
                    s = 'font-weight:bold;'
                    styles.append(s)
                else:
                    print(f'unknown style setting: {style["style"]}')
        
        # return as a long string
        return "".join(styles)