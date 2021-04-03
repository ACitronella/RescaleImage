import cv2
import os
import argparse

# dataset_dir = ".\\food-dataset"
# new_dir = ".\\food-dataset-copy"


def resize_img(img_dir: str, new_dir: str, img_size: tuple):
    isError = False
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    if not os.path.exists(new_dir+img_dir[1:]):
        os.mkdir(new_dir+img_dir[1:])

    dirs = [f.path for f in os.scandir(img_dir)]
    for d in dirs:
        foods = [f.path for f in os.scandir(d)]

        if not os.path.exists(new_dir+d[1:]):
            os.mkdir(new_dir+d[1:])
        
        for food in foods:
            imgs = [f.path for f in os.scandir(food)]

            if not os.path.exists(new_dir+food[1:]):
                os.mkdir(new_dir+food[1:])

            for img_path in imgs:
                image = cv2.imread(img_path)
                new_path = new_dir + img_path[1:]
                try:
                    res = cv2.resize(image, dsize=img_size, interpolation=cv2.INTER_CUBIC)
                    # print("writing on path: ", new_path)
                    assert cv2.imwrite(new_path, res)
                except cv2.error as e:
                    print("problem occur in", new_path, e)
                    isError = True
    print("resize image complete")
    if isError:
        print("there is some error, check")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--imgdir", type=str, required=True, help="Directory of starting dataset")
    parser.add_argument("--newdir", type=str, default="", help="Target directory of tranformed dataset")
    parser.add_argument("--imgsize", type=str, help="Tuple of image output size for ex. (256, 256)", default="(256, 256)")
    args = parser.parse_args()
    
    newdir = ""
    img_size = eval(args.imgsize)
    if args.newdir == "":
        newdir = args.imgdir + "-" + str(img_size[0]) + "-" + str(img_size[1])
    else:
        newdir = args.newdir

    assert len(img_size) == 2
    resize_img(args.imgdir, newdir, img_size)


    
