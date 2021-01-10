class ScourStats(object):

    __slots__ = (
        'num_elements_removed',
        'num_attributes_removed',
        'num_style_properties_fixed',
        'num_bytes_saved_in_colors',
        'num_ids_removed',
        'num_comments_removed',
        'num_style_properties_fixed',
        'num_rasters_embedded',
        'num_path_segments_removed',
        'num_points_removed_from_polygon',
        'num_bytes_saved_in_path_data',
        'num_bytes_saved_in_colors',
        'num_bytes_saved_in_comments',
        'num_bytes_saved_in_ids',
        'num_bytes_saved_in_lengths',
        'num_bytes_saved_in_transforms',
    )

    def __init__(self):
        self.reset()

    def reset(self):
        # Set all stats to 0
        for attr in self.__slots__:
            setattr(self, attr, 0)
