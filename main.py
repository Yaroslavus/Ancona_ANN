import pathlib
import json
from dataclasses import dataclass
from PIL import Image, ImageDraw
from itertools import chain
import cv2


@dataclass(frozen=True)
class GlobalPathes:
    data_path: pathlib.WindowsPath = pathlib.Path(__file__).parent.joinpath('DATA')
    test_path: pathlib.WindowsPath = data_path.joinpath('test')
    train_path: pathlib.WindowsPath = data_path.joinpath('train_brain')
    trans_cerebellum_test_path: pathlib.WindowsPath = test_path.joinpath('Trans-cerebellum')
    trans_thalamic_test_path: pathlib.WindowsPath = test_path.joinpath('Trans-thalamic')
    trans_ventricular_test_path: pathlib.WindowsPath = test_path.joinpath('Trans-ventricular')
    trans_cerebellum_train_path: pathlib.WindowsPath = train_path.joinpath('Trans-cerebellum')
    trans_thalamic_train_path: pathlib.WindowsPath = train_path.joinpath('Trans-thalamic')
    trans_ventricular_train_path: pathlib.WindowsPath = train_path.joinpath('Trans-ventricular')
    out_path: pathlib.WindowsPath = data_path.parent.joinpath('OUT')
    out_test_path: pathlib.WindowsPath = out_path.joinpath('test')
    out_train_path: pathlib.WindowsPath = out_path.joinpath('train_brain')
    trans_cerebellum_out_test_path: pathlib.WindowsPath = out_test_path.joinpath('Trans-cerebellum')
    trans_thalamic_out_test_path: pathlib.WindowsPath = out_test_path.joinpath('Trans-thalamic')
    trans_ventricular_out_test_path: pathlib.WindowsPath = out_test_path.joinpath('Trans-ventricular')
    trans_cerebellum_out_train_path: pathlib.WindowsPath = out_train_path.joinpath('Trans-cerebellum')
    trans_thalamic_out_train_path: pathlib.WindowsPath = out_train_path.joinpath('Trans-thalamic')
    trans_ventricular_out_train_path: pathlib.WindowsPath = out_train_path.joinpath('Trans-ventricular')
    in_path_dict = {"data_path": data_path,
                    "test_path": test_path,
                    "train_path": train_path,
                    "trans_cerebellum_test_path": trans_cerebellum_test_path,
                    "trans_thalamic_test_path": trans_thalamic_test_path,
                    "trans_ventricular_test_path": trans_ventricular_test_path,
                    "trans_cerebellum_train_path": trans_cerebellum_train_path,
                    "trans_thalamic_train_path": trans_thalamic_train_path,
                    "trans_ventricular_train_path": trans_ventricular_train_path}
    out_path_dict = {"out_path": out_path,
                     "out_test_path": out_test_path,
                     "out_train_path": out_train_path,
                     "trans_cerebellum_out_test_path": trans_cerebellum_out_test_path,
                     "trans_thalamic_out_test_path": trans_thalamic_out_test_path,
                     "trans_ventricular_out_test_path": trans_ventricular_out_test_path,
                     "trans_cerebellum_out_train_path": trans_cerebellum_out_train_path,
                     "trans_thalamic_out_train_path": trans_thalamic_out_train_path,
                     "trans_ventricular_out_train_path": trans_ventricular_out_train_path}

    for path in out_path_dict.values():
        if not path.exists(): path.mkdir(parents = False, exist_ok = False)

    def __str__(self):
        return "\n".join([f'{key}:\t{str(value)}' for key, value in chain(
            self.in_path_dict.items(), self.out_path_dict.items())])


@dataclass(frozen=True)
class ImageDescription:
    version: str
    flags: dict
    shapes: list
    imagePath: str
    imageData: str
    imageHeight: int
    imageWidth: int


@dataclass(frozen=True)
class ImagePath:
    description_file: pathlib.WindowsPath
    input_image_file: pathlib.WindowsPath
    output_image_file: pathlib.WindowsPath


def draw_shapes_and_labels(image_file: str) -> None:
    file = pathlib.Path(image_file)
    image_pathes = ImagePath(description_file=pathes.data_path.joinpath(file.with_suffix(".json")),
                             input_image_file=pathes.data_path.joinpath(file.with_suffix(".png")),
                             output_image_file=pathes.out_path.joinpath(file.with_suffix(".png")))
    with open(image_pathes.description_file) as fin:
        t = json.load(fin)

    Image_info = ImageDescription(version=t["version"], flags=t["flags"], shapes=t["shapes"],
                                  imagePath=t["imagePath"], imageData=t["imageData"],
                                  imageHeight=t["imageHeight"], imageWidth=t["imageWidth"])

    Image_object = Image.open(image_pathes.input_image_file)
    draw = ImageDraw.Draw(Image_object)
    for shape in Image_info.shapes:
        if shape["shape_type"] == "rectangle":
            points = shape["points"]
            points_tuple = tuple([*points[0], *points[1]])
            draw.rectangle(points_tuple, outline="red")
            draw.text(points_tuple[:2], text=shape["label"])
            Image_object.save(image_pathes.output_image_file, "JPEG")


if __name__ =="__main__":
    pathes = GlobalPathes()
    # draw_shapes_and_labels("test/Trans-cerebellum/Patient00644_Plane3_2_of_3")
    print(pathes)



