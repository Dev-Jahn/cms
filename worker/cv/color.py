import cv2


def grayscale(src):
    res = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    return res


def apply(src, method):
    if method == 'gray':
        return grayscale(src)
    else:
        raise KeyError('Wrong function name')