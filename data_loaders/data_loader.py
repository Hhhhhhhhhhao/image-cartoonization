from torchvision import transforms
from base import BaseDataLoader
from torch.utils.data import DataLoader
from .datasets import CartoonDataset, CartoonGANDataset, CartoonDefaultDataset, StarCartoonDataset, ClassifierDataset
from torchvision.datasets import ImageFolder


def build_train_transform(style='real', image_size=256):
    if style == 'real':
        transform = transforms.Compose([
            transforms.RandomResizedCrop(image_size, scale=(0.5, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
    else:

        transform = transforms.Compose([
            transforms.RandomCrop(512),
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
    return transform


def build_test_transform(style='real', image_size=256):
    if style == 'real':
        transform = transforms.Compose([
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
    else:
        transform = transforms.Compose([
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
    return transform


class CartoonDefaultDataLoader(DataLoader):
    def __init__(self, data_dir, style='real', image_size=256, batch_size=16, num_workers=4):
        transform = build_test_transform(style, image_size)
        self.dataset = CartoonDefaultDataset(data_dir=data_dir, style=style, transform=transform)
        super(CartoonDefaultDataLoader, self).__init__(
            dataset=self.dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            drop_last=True)


class CartoonDataLoader(BaseDataLoader):
    def __init__(self, data_dir, src_style='real', tar_style='gongqijun', image_size=256, batch_size=16, num_workers=4, validation_split=0.01):

        # data augmentation
        src_transform = build_train_transform(src_style, image_size)
        tar_transform = build_train_transform(tar_style, image_size)

        # create dataset
        self.dataset = CartoonDataset(data_dir, src_style, tar_style, src_transform, tar_transform)

        super(CartoonDataLoader, self).__init__(
            dataset=self.dataset,
            batch_size=batch_size,
            shuffle=True,
            validation_split=validation_split,
            num_workers=num_workers,
            drop_last=True)

    def shuffle_dataset(self):
        self.dataset._shuffle_data()


class CartoonGANDataLoader(BaseDataLoader):
    def __init__(self, data_dir, src_style='real', tar_style='gongqijun', image_size=256, batch_size=16, num_workers=4, validation_split=0.01):

        # data augmentation
        src_transform = build_train_transform(src_style, image_size)
        tar_transform = build_train_transform(tar_style, image_size)

        # create dataset
        self.dataset = CartoonGANDataset(data_dir, src_style, tar_style, src_transform, tar_transform)

        super(CartoonGANDataLoader, self).__init__(
            dataset=self.dataset,
            batch_size=batch_size,
            shuffle=True,
            validation_split=validation_split,
            num_workers=num_workers,
            drop_last=True)

    def shuffle_dataset(self):
        self.dataset._shuffle_data()


class StarCartoonDataLoader(BaseDataLoader):
    def __init__(self, data_dir, image_size=256, batch_size=16, num_workers=4, validation_split=0.01):
        # data augmentation
        src_transform = build_train_transform('real', image_size)
        tar_transform = build_train_transform('cartoon', image_size)

        # create dataset
        self.dataset = StarCartoonDataset(data_dir, src_transform, tar_transform)
        super(StarCartoonDataLoader, self).__init__(
            dataset=self.dataset,
            batch_size=batch_size,
            shuffle=True,
            validation_split=validation_split,
            num_workers=num_workers,
            drop_last=True)

    def shuffle_dataset(self):
        self.dataset._shuffle_data()


class ClassifierDataLoader(BaseDataLoader):
    def __init__(self, data_dir, split, image_size=256, batch_size=16, num_workers=4, validation_split=0.01):

        transform = transforms.Compose([
            transforms.RandomResizedCrop(image_size, scale=(0.5, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])

        # create dataset
        self.dataset = ClassifierDataset(data_dir, split, transform)

        super(ClassifierDataLoader, self).__init__(
            dataset=self.dataset,
            batch_size=batch_size,
            shuffle=True,
            validation_split=validation_split,
            num_workers=num_workers,
            drop_last=True)


if __name__ == '__main__':
    data_dir = '/Users/leon/Downloads/cartoon_datasets'
    style = 'gongqijun'
    data_loader = CartoonDataLoader(data_dir)
    valid_dataloader = data_loader.split_validation()

    for i, (src_img, tar_img) in enumerate(data_loader):
        print(src_img.shape)
        print(tar_img.shape)

