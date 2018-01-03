import cv2


def draw_lines(source_img, lines):
    if (len(lines) == 0):
        return
    for line in lines:
        if line is not None:
            coords = line[0]
            cv2.line(source_img, (coords[0], coords[1]), (coords[2], coords[3]),
                     [100, 255, 0], 10)


def draw_obstacles(color_img, contours):
    cv2.drawContours(color_img, contours, -1, (255, 255, 255), 3)


def draw_obstacles_points(color_img, obstacles, obstacles_world):
    for i in range(len(obstacles)):
        obs = obstacles[i]
        obs_world = obstacles_world[i]
        # if obs_world.is_real:
        cv2.circle(color_img, (obs[0] - 23, obs[2]), 5, (255, 0, 0), thickness=-1)
        cv2.circle(color_img, (obs[1] - 23, obs[2]), 5, (255, 0, 255), thickness=-1)
        cv2.putText(color_img, '{:1.2f} {}'.format(obs[3], obs_world.is_real),
                    (obs[0], obs[2]), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 0))
        cv2.putText(color_img, '{}'.format(str(obs_world)),
                    (obs[0] - 40, obs[2] + 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 0))

def display(img_name, img):
    img2 = cv2.resize(img, (640, 480))
    cv2.imshow(img_name, img2)
    cv2.waitKey(1)


def display_image_with_lines(im, left, right):
    im_w_lines = im.copy()
    draw_lines(im_w_lines, [left, right])
    display('image with lines', im_w_lines)
