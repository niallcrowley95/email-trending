import jinja2


def get_render(style,
               sections,
               loc="./templates/",
               template_file="template.html"):
    """
    Render full html email template

    Args:
    - style -- css style in dict format
    - sections -- dict containing sections to be filled in the body of the email
    - loc -- folder to look for template (default ./templates/)
    - template_file -- name of html template file to fill (default template.html)
    """
    # get file
    template_loader = jinja2.FileSystemLoader(searchpath=loc)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file)

    # fill file with css and content
    output = template.render(style=style, sections=sections)
    return output
