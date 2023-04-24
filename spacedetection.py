import cv2 as open_cv
import numpy as np

#from colors import COLOR_WHITE
from drawing_utils import draw_contours

COLOR_WHITE = (255, 255, 255)


class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, output, color):
        self.output = output
        self.caption = image
        self.color = color

        self.image = open_cv.imread(image).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []

        open_cv.namedWindow(self.caption, open_cv.WINDOW_NORMAL)
        open_cv.setMouseCallback(self.caption, self.__mouse_callback)

    def generate(self):
        print('Starting generate')
        while True:
            open_cv.resizeWindow(self.caption, 800, 600)
            # Resize the image to fit inside the window
            height, width, channels = self.image.shape
            scale_factor = min(1, 800/width, 600/height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            resized_image = open_cv.resize(self.image, (new_width, new_height))
            open_cv.imshow(self.caption, self.image)
            
            print('Window Displayed')
            key = open_cv.waitKey(0)

            if key == CoordinatesGenerator.KEY_RESET:
                self.image = self.image.copy()
            elif key == CoordinatesGenerator.KEY_QUIT:
                break
        print('Window destroying')
        open_cv.destroyWindow(self.caption)

    def __mouse_callback(self, event, x, y, flags, params):

        if event == open_cv.EVENT_LBUTTONDOWN:
            self.coordinates.append((x, y))
            self.click_count += 1

            if self.click_count >= 4:
                self.__handle_done()

            elif self.click_count > 1:
                self.__handle_click_progress()

        open_cv.imshow(self.caption, self.image)

    def __handle_click_progress(self):
        open_cv.line(self.image, self.coordinates[-2], self.coordinates[-1], (255, 0, 0), 1)

    def __handle_done(self):
        open_cv.line(self.image,
                     self.coordinates[2],
                     self.coordinates[3],
                     self.color,
                     1)
        open_cv.line(self.image,
                     self.coordinates[3],
                     self.coordinates[0],
                     self.color,
                     1)

        self.click_count = 0

        coordinates = np.array(self.coordinates)

        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                          "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                          "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                          "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                          "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")

        draw_contours(self.image, coordinates, str(self.ids + 1), COLOR_WHITE)

        for i in range(0, 4):
            self.coordinates.pop()

        self.ids += 1

def main():
    image = r'C:\Users\Joey\OneDrive - University of Miami\Seventh Semester\Senior Design\yolov5-master\imgs\Senior Design Images\1.png'
    coord_file = 'coords.yaml'
    #Up to here, the code is collecting coordinates of the parking spaces
    if image is not None:
        with open(coord_file, "w+") as coords:
            gen = CoordinatesGenerator(image, coords, (0, 0, 255))
            gen.generate()

if __name__ == "__main__":
    main()
