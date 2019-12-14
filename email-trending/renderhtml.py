import jinja2


def get_render(style,
               sections,
               quote,
               loc="./templates/",
               template_file="template.html"):
    """
    Render full html email template

    Args:
    - style -- css style in dict format
    - sections -- dict containing sections to be filled in the body of the email
    - loc -- folder to look for template
    - template_file -- name of html template file to fill
    """
    # get file
    template_loader = jinja2.FileSystemLoader(searchpath=loc)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file)

    # fill file with css and content
    output = template.render(style=style, sections=sections, quote=quote)
    return output


def get_render_markets(style,
                       sections,
                       markets,
                       quote,
                       loc="./templates/",
                       template_file="template_markets.html"):
    """
    Render full html email template

    Args:
    - style -- css style in dict format
    - sections -- dict containing sections to be filled in the body of the email
    - markets -- dict containing tickers, price and daily change
    - loc -- folder to look for template
    - template_file -- name of html template file to fill
    """
    # get file
    template_loader = jinja2.FileSystemLoader(searchpath=loc)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file)

    # fill file with css and content
    output = template.render(style=style, sections=sections, markets=markets, quote=quote)
    return output
