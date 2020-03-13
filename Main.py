import NodeGrid as ng
import time
import ImageReader


image_to_process = 'Example.png'  # white - plain, black - obstacle, red - start, blue - target
image_to_save = 'ExamplePath.png'  # green - path


def display_grid():
    start_time = time.time()

    print("Reading image")
    matrix, (start_x, start_y), (end_x, end_y) = ImageReader.read_image(image_to_process)

    print("Setting nodes")
    node_grid = ng.NodeGrid(matrix)
    node_grid.set_start(start_x, start_y)
    node_grid.set_end(end_x, end_y)

    print("Finding path")
    path = node_grid.find_path()

    print("Path found")
    print("Drawing path")
    ImageReader.draw_path(image_to_process, image_to_save, path)

    print("Finished")

    elapsed_time = time.time() - start_time
    print('{} seconds elapsed'.format(elapsed_time))


if __name__ == '__main__':
    display_grid()