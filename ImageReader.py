from PIL import Image

plain = 255, 255, 255, 255
start = 255, 0, 0, 255
end = 0, 0, 255, 255
obstacle = 0, 0, 0, 255
path_colour = 50, 180, 50


def read_image(image_name):
    matrix = []
    start_x, start_y = 0, 0
    end_x, end_y = 0, 0
    im = Image.open(image_name, 'r')
    width, height = im.size
    for i in range(height):
        matrix.append([])
        for j in range(width):
            pixel = im.getpixel((j, i))
            if pixel == plain:
                matrix[i].append(0)
            elif pixel == obstacle:
                matrix[i].append(1)
            elif pixel == start:
                matrix[i].append(0)
                start_x, start_y = j, i
            elif pixel == end:
                matrix[i].append(0)
                end_x, end_y = j, i
    im.close()
    return matrix, (start_x, start_y), (end_x, end_y)


def draw_path(image_name, save_name, path):
    im = Image.open(image_name, 'r')
    for node in path:
        im.putpixel((node.x, node.y), path_colour)
    im.save(save_name)
    im.close()
