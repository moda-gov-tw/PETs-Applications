import numpy as np

from nvflare.apis.filter import Filter
from nvflare.apis.fl_constant import FLConstants, ShareableKey, ShareableValue
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable

class RandomExclude(Filter):
    
    def __init__(self):
        super().__init__()
    
    def process(self, shareable: Shareable, fl_ctx: FLContext) -> Shareable:
        ratio = 0.5
        # get model weights
        weights = shareable[ShareableKey.MODEL_WEIGHTS]
        # set excluded variables to all zeros
        var_names = list(weights.keys())
        n_vars = len(var_names)
        np.random.shuffle(var_names)
        n_excluded = int(n_vars*ratio)
        exclude_vars = var_names[:n_excluded]
        for var_name in var_names:
            if var_name in exclude_vars:
                weights[var_name] = np.zeros(weights[var_name].shape) 
        self.logger.info(f"Excluded {n_excluded} of {n_vars} variables")
        shareable[ShareableKey.MODEL_WEIGHTS] = weights        
        return shareable