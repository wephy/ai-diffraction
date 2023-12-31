import os.path
from data.base_dataset import BaseDataset, get_params, get_transform, normalize
from data.image_folder import make_dataset
from torchvision.transforms import transforms
import cv2


class AlignedDataset(BaseDataset):
    def initialize(self, opt):
        self.opt = opt
        self.phase = opt.phase
        self.root = opt.dataroot
        self.input = opt.input
        self.split = opt.split
        self.ICSD_codes = os.listdir(self.root)
        self.paths = {}

        with open(os.path.join(self.split, "train")) as file:
            self.paths["train"] = file.read().split("\n")[:-1]
        with open(os.path.join(self.split, "val")) as file:
            self.paths["val"] = file.read().split("\n")[:-1]
        with open(os.path.join(self.split, "test")) as file:
            self.paths["test"] = file.read().split("\n")[:-1]

        self.dataset_size = len(self.paths[self.phase])

    def __getitem__(self, index):
        ICSD_code = self.paths[self.phase][index]
        transform = transforms.ToTensor()

        if self.input == "structure":
            A_path = os.path.join(self.root, ICSD_code, ICSD_code + "_structure.png")
            B_path = os.path.join(self.root, ICSD_code, ICSD_code + "_+0+0+0.png")
        elif self.input == "pattern":
            A_path = os.path.join(self.root, ICSD_code, ICSD_code + "_+0+0+0.png")
            B_path = os.path.join(self.root, ICSD_code, ICSD_code + "_structure.png")
        else:
            raise ValueError("input must be 'structure' or 'pattern'")
        A = cv2.imread(A_path)
        A_tensor = transform(A)

        B_tensor = 0
        if self.opt.isTrain:
            B = cv2.imread(B_path)
            B_tensor = transform(B)

        input_dict = {
            "label": A_tensor,
            "inst": 0,
            "image": B_tensor,
            "feat": 0,
            "path": A_path,
        }

        return input_dict

    def __len__(self):
        return len(self.paths[self.phase]) // self.opt.batchSize * self.opt.batchSize

    def name(self):
        return "AlignedDataset"
