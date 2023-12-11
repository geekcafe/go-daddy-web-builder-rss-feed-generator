

class HtmlCreator:
    @staticmethod
    def create_html_from_json_content(json_data):
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
    
    def get_content_from_block(block):
        text = block["text"]
        html = None
        if text:
            style = HtmlCreator.get_sytle_from_block(block)
            html = f"<p><span style=\"{style}\">{text}</span></p>"
            

        return html

    def get_sytle_from_block(block):
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