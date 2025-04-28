from typing import Tuple, List
import numpy as np
class Segement:
    name: str
    mask: np.ndarray
    color: Tuple[int, int, int]

    def __init__(self, name:str, volume_size: Tuple[int,int, int], color: Tuple[int, int, int]) -> None:

        self.name = name;
        self.mask = np.zeros(volume_size, dtype=np.int32)
        self.color = color

    def apply_mask_update(self, new_mask:np.ndarray, op:str = "add"):
        """Apply a mask operation
        this method assumes that new_mask and mask have the same dimensions
        """
        if op == "add":
            # adding a new mask
            self.mask = np.logical_or(self.mask, new_mask)
        elif op == "subtract":
            # subtracting mask by new mask 
            # mask = mask - new_mask
            self.mask = np.logical_and(self.mask, ~new_mask)
            pass
        elif op == "replace":
            # replace mask with new mask
            # mask = new_mask
            self.mask[:] = new_mask
        else:
            raise ValueError("Invalid mode: only add, subtract, replace are supported")






