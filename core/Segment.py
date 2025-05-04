from typing import Tuple, List
import numpy as np
class Segment:
    name: str
    mask: np.ndarray
    color: Tuple[int, int, int]
    volume_size:Tuple[int,int,int]

    def __init__(self, name:str, volume_size: Tuple[int,int, int], color: Tuple[int, int, int]) -> None:

        self.name = name;
        self.mask = np.zeros(volume_size, dtype=np.int8)

        self.color = color
        self.volume_size = volume_size

    def __str__(self) -> str:
        return f"Segement: {self.name}\n Size: {self.volume_size}\n Color: {self.color}\n Mask:{self.mask}"

    def apply_mask_update(self, new_mask:np.ndarray, op:str = "add"):
        """Apply a mask operation
        this method assumes that new_mask and mask have the same dimensions
        """
        if op == "add":
            # adding a new mask
            self.mask = np.logical_or(self.mask, new_mask).astype(np.int8)
        elif op == "subtract":
            # subtracting mask by new mask 
            # mask = mask - new_mask
            self.mask = np.logical_and(self.mask, ~new_mask).astype(np.int8)
        elif op == "replace":
            # replace mask with new mask
            # mask = new_mask
            self.mask[:] = new_mask.astype(np.int8)
        else:
            raise ValueError("Invalid mode: only add, subtract, replace are supported")






