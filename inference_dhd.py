import cv2
import numpy as np
import os
import torch
from basicsr.utils import imwrite

from gfpgan import GFPGANer


class Args:
    aligned = False
    bg_tile = 400
    bg_upsampler = 'realesrgan'
    ext = 'auto'
    only_center_face = False
    suffix = None
    upscale = 2
    version = '1.3'
    weight = 0.5


class ImageRestorer:
    def __init__(self):
        """
            Inference demo for GFPGAN (for users).
        """
        self.args = Args()

        # ------------------------ set up background upsampler ------------------------
        if self.args.bg_upsampler == 'realesrgan':
            if not torch.cuda.is_available():  # CPU
                import warnings
                warnings.warn('The unoptimized RealESRGAN is slow on CPU. We do not use it. '
                              'If you really want to use it, please modify the corresponding codes.')
                bg_upsampler = None
            else:
                from basicsr.archs.rrdbnet_arch import RRDBNet
                from realesrgan import RealESRGANer
                model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
                bg_upsampler = RealESRGANer(
                    scale=2,
                    model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth',
                    model=model,
                    tile=self.args.bg_tile,
                    tile_pad=10,
                    pre_pad=0,
                    half=True)  # need to set False in CPU mode
        else:
            bg_upsampler = None

        # ------------------------ set up GFPGAN restorer ------------------------
        arch = 'clean'
        channel_multiplier = 2
        model_name = 'GFPGANv1.3'
        # determine model paths
        model_path = os.path.join('experiments/pretrained_models', model_name + '.pth')

        self.restorer = GFPGANer(
            model_path=model_path,
            upscale=self.args.upscale,
            arch=arch,
            channel_multiplier=channel_multiplier,
            bg_upsampler=bg_upsampler)

        print("Load model done.")

    def inference(self, image):
        """
            restore input image
        Args:
            image: image opened by opencv
        Returns: restored image
        """
        cropped_faces, restored_faces, restored_img = self.restorer.enhance(
            image,
            has_aligned=self.args.aligned,
            only_center_face=self.args.only_center_face,
            paste_back=True,
            weight=self.args.weight)

        output_image = cv2.resize(restored_img, None, fx=0.5, fy=0.5)

        return output_image


if __name__ == '__main__':
    restorer = ImageRestorer()

    test_image_dir = "./inputs/self_test_images"
    for test_image_name in os.listdir(test_image_dir):
        test_image_path = os.path.join(test_image_dir, test_image_name)
        input_img = cv2.imread(test_image_path, cv2.IMREAD_COLOR)
        print(input_img.shape)

        output_img = restorer.inference(input_img)
        print(output_img.shape)

        output_path = os.path.join("./results", os.path.basename(test_image_path))
        cv2.imwrite(output_path, output_img)
