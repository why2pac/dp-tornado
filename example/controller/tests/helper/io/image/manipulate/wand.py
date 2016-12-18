# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class WandController(Controller):
    def get(self):
        # Image from URL

        """
        image_url = 'http://httpbin.org/image/png'
        image_obj = self.helper.io.image.load(image_url)
        image_size = self.helper.io.image.size(image_obj)

        assert image_size and len(image_size) == 2
        """

        # Image from Filepath

        image_path = self.ini.server.application_path
        image_path = self.helper.io.path.join(image_path, 'static', 'tests', 'helper', 'io', 'image')
        sample_path = self.helper.io.path.join(image_path, 'sample.jpg')

        image_obj = self.helper.io.image.load(sample_path, **{'driver': 'wand'})
        image_size = self.helper.io.image.size(image_obj)

        assert image_size and len(image_size) == 2

        image_width, image_height = image_size

        # Crop (all)

        crop = 10
        cropped_img = self.helper.io.image.manipulate(sample_path, **{'driver': 'wand', 'crop': crop})

        assert cropped_img.size[0] == image_width - (crop * 2) and cropped_img.size[1] == image_height - (crop * 2)

        # Crop (vertiacal and horizontal)

        crop_v = 10
        crop_h = 20
        cropped_img = self.helper.io.image.manipulate(
            sample_path,
            **{
                'driver': 'wand',
                'crop': '%s, %s' % (crop_v, crop_h)})

        assert cropped_img.size[0] == image_width - (crop_h * 2) and cropped_img.size[1] == image_height - (crop_v * 2)

        # Crop (top, right, bottom, left)

        crop_t = 10
        crop_r = 20
        crop_b = 30
        crop_l = 40
        cropped_img = self.helper.io.image.manipulate(
            image_obj,
            **{
                'driver': 'wand',
                'crop': (crop_t, crop_r, crop_b, crop_l)})

        assert(cropped_img.size[0] == image_width - (crop_r + crop_l) and
               cropped_img.size[1] == image_height - (crop_t + crop_b))

        # Test

        save_prefix = 'dp_image_test'

        self.helper.io.path.mkdir(save_prefix)

        # Crop

        cropped_img_compare = self.helper.io.path.join(image_path, 'compare', 'crop.png')
        cropped_img_dest = '%s/crop.png' % save_prefix

        assert self.helper.io.image.manipulate(
            sample_path,
            **{
                'driver': 'wand',
                'crop': '27,10,15,10',
                'dest': cropped_img_dest})
        assert self.helper.io.image.compare(cropped_img_dest, cropped_img_compare, error=3)

        # Border

        bordered_img_compare = self.helper.io.path.join(image_path, 'compare', 'border.png')
        bordered_img_dest = '%s/border.png' % save_prefix

        try:
            self.helper.io.image.manipulate(
                sample_path, **{
                    'driver': 'wand',
                    'border': 2,
                    'border_color': '#ff0000',
                    'dest': bordered_img_dest})
            assert False, 'Not implemented method.'
        except:
            assert True

        # Radius

        radius_img_compare = self.helper.io.path.join(image_path, 'compare', 'radius.png')
        radius_img_dest = '%s/radius.png' % save_prefix

        try:
            self.helper.io.image.manipulate(
                sample_path,
                **{
                    'driver': 'wand',
                    'radius': 100,
                    'dest': radius_img_dest})
            assert False, 'Not implemented method.'
        except:
            assert True

        # Radius with border

        radius_wb_img_compare = self.helper.io.path.join(image_path, 'compare', 'radius_wb.png')
        radius_wb_img_dest = '%s/radius_wb.png' % save_prefix

        try:
            self.helper.io.image.manipulate(
                sample_path,
                **{
                    'driver': 'wand',
                    'radius': 100,
                    'border': 2,
                    'border_color': '#ff0000',
                    'dest': radius_wb_img_dest})
            assert False, 'Not implemented method.'
        except:
            assert True

        # Resize

        resize_img_compare = self.helper.io.path.join(image_path, 'compare', 'resize.png')
        resize_img_dest = '%s/resize.png' % save_prefix

        assert self.helper.io.image.manipulate(
            sample_path,
            **{
                'driver': 'wand',
                'size': (80, 150),
                'dest': resize_img_dest})
        assert self.helper.io.image.compare(resize_img_dest, resize_img_compare, error=15)

        # Resize - center w/ radius

        resize_img_compare = self.helper.io.path.join(image_path, 'compare', 'resize_center_wr.png')
        resize_img_dest = '%s/resize_center_wr.png' % save_prefix

        try:
            assert self.helper.io.image.manipulate(
                sample_path,
                **{
                    'driver': 'wand',
                    'size': (80, 150),
                    'background': '#00ff00',
                    'radius': 50,
                    'mode': self.helper.io.image.mode.center,
                    'dest': resize_img_dest})
            assert False, 'Not implemented method.'
        except:
            assert True

        # Resize - center

        resize_img_compare = self.helper.io.path.join(image_path, 'compare', 'resize_center.png')
        resize_img_dest = '%s/resize_center.png' % save_prefix

        try:
            self.helper.io.image.manipulate(
                sample_path,
                **{
                    'driver': 'wand',
                    'size': (80, 150),
                    'background': '#ff0000',
                    'mode': self.helper.io.image.mode.center,
                    'dest': resize_img_dest})
            assert False, 'Not implemented method.'
        except:
            assert True

        # Resize - fill

        resize_img_compare = self.helper.io.path.join(image_path, 'compare', 'resize_fill.png')
        resize_img_dest = '%s/resize_fill.png' % save_prefix

        assert self.helper.io.image.manipulate(
            sample_path,
            **{
                'driver': 'wand',
                'size': (80, 150),
                'mode': self.helper.io.image.mode.fill,
                'dest': resize_img_dest})
        assert self.helper.io.image.compare(resize_img_dest, resize_img_compare, error=3)

        self.helper.io.file.remove(save_prefix)

        self.finish('done')
