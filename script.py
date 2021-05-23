import cv2
import os
import argparse

class RecursiveResize:

    __count = 0 

    @staticmethod
    def recursive_resize(img_dir: str, new_dir: str, img_size: tuple):
        if not os.path.exists(new_dir):
            print("not found target directory, creating one at", new_dir)
            os.mkdir(new_dir)
        d = os.path.join(new_dir, img_dir)
        if not os.path.exists(d):
            os.mkdir(d)
        RecursiveResize.__recursive_resize(img_dir, new_dir, img_size)

        print("resized", RecursiveResize.__count, "image")
        RecursiveResize.__count = 0

    @staticmethod
    def __recursive_resize(img_dir: str, new_dir: str, img_size: tuple):
        dirs = [f.path for f in os.scandir(img_dir)]
        for path in dirs:
            new_dataset_path = os.path.join(new_dir, path)
            if os.path.isdir(path):
                if not os.path.exists(new_dataset_path):
                    os.mkdir(new_dataset_path)
                RecursiveResize.__recursive_resize(path, new_dir, img_size)
            else:
                try:
                    image = cv2.imread(path)
                    img_res = cv2.resize(image, dsize=img_size, interpolation=cv2.INTER_CUBIC)
                    # print(new_dataset_path)
                    assert cv2.imwrite(new_dataset_path, img_res)
                    RecursiveResize.__count = RecursiveResize.__count + 1
                    
                except cv2.error as e:
                    print("problem occur in", new_dataset_path, e)


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
    
    RecursiveResize.recursive_resize(args.imgdir, newdir, img_size)
