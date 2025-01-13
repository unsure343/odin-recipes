import argparse
import yaml
import os
import traceback

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yml", type=str)
    parser.add_argument("-o", "--output", type=str)
    return parser.parse_args()

def get_recipe_from_yml(yml: str) -> dict:
    with open(yml, "r", encoding="utf-8") as fs:
        try:
            recipe = yaml.safe_load(fs)
        except yaml.YAMLError as exc:
            print(traceback.format_exc())
            exit(-1)
    return recipe

def get_html_header(name: str) -> str:
    return """<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{}</title>
        </head>
<body>
    <h1>{}</h1>
    """.format(name, name)

def get_required_element(input_dict: dict, key: str) -> str:
    try:
        elem = input_dict[key]
    except KeyError as exc:
        print(f"Could not find required key {key} in dict {input_dict}.")
        print(f"Please provide a valid {key}!")
        print(traceback.format_exc())
        exit(-1)
    if not elem:
        print(f"Please provide a valid value for key {key}")
        exit(-1)
    if str(elem).isnumeric():
        return f" {key}={elem}"
    else:
        return f" {key}=\"{elem}\""

def get_unrequired_element(input_dict: dict, key: str) -> str:
    elem = input_dict.get(key)
    if elem:
        if str(elem).isnumeric():
            return f" {key}={elem}"
        else:
            return f" {key}=\"{elem}\""
    return ""

def get_image_string(image: dict) -> str:
    text = ["<img"]
    text.append(get_required_element(image, "src"))
    text.append(" ")
    text.append(get_required_element(image, "alt"))
    text.append(get_unrequired_element(image, "height"))
    text.append(get_unrequired_element(image, "width"))
    text.append(">\n")
    return "".join(text)

def get_description(description: str) -> str:
    return f"    <h2>Description</h2>\n    {description}\n"

def get_ingredients(ingredients: list) -> str:
    ingredient_list = ["<h2>Ingredients</h2>\n", "<ul>\n"]
    for ingredient in ingredients:
        ingredient_list.append(f"    <li>{ingredient}</li>\n")
    ingredient_list.append("</ul>\n")
    return "    ".join(ingredient_list)

def get_directions(directions: list) -> str:
    directions_list = ["<h2>Directions</h2>\n", "<ol>\n"]
    for direction in directions:
        directions_list.append(f"    <li>{direction}</li>\n")
    directions_list.append("</ol>\n")
    return "    ".join(directions_list)

def link_to_home() -> str:
    return "        <br>\n    <a href=\"../index.html\">Home</a>\n"

def write_output(html_out: str, output: str):
    with open(output, "w", encoding="utf-8") as out:
        out.write(html_out)

def convert_yml_to_html(yml, output):
    recipe = get_recipe_from_yml(yml)
    string_list = [get_html_header(recipe["name"])]
    string_list.append(get_image_string(recipe["image"]))
    string_list.append(get_description(recipe["description"]))
    string_list.append(get_ingredients(recipe["ingredients"]))
    string_list.append(get_directions(recipe["directions"]))
    string_list.append(link_to_home())
    string_list.append("</body>\n</html>")
    html_out = "".join(string_list)
    write_output(html_out, output)
    

if __name__ == "__main__":
    args = get_args()
    convert_yml_to_html(args.yml, args.output)