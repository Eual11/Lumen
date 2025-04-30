from typing import List, Optional
from vtk import vtkAlgorithmOutput, vtkCubeSource
from vtk import vtkAlgorithm


class DynamicPipeline :
    def __init__(self, source:Optional[vtkAlgorithmOutput]=None) -> None:
        # input and output of pipelin
        self.source = source
        self.ouputport :Optional[vtkAlgorithmOutput]= None

        self.filters:List[vtkAlgorithm] =[]

        self._rebuild_pipeline()

    def _rebuild_pipeline(self):
        if not self.source:
            return
        current:vtkAlgorithm = self.source.GetProducer()

        for f in self.filters:
            f.SetInputConnection(current.GetOutputPort())

            current = f
        self.ouputport:Optional[vtkAlgorithmOutput] = current.GetOutputPort()
            
    def add_filter(self, filter:vtkAlgorithm, index =None):
        if not index:
            self.filters.append(filter)
        else:
            self.filters.insert(index, filter)
        self._rebuild_pipeline()

    def remove_filter(self,index:int):

        if(0<=index <len(self.filters)):
            del self.filters[index]
        self._rebuild_pipeline()
    

    def get_ouput_port(self):
        return self.ouputport
    def get_output_data(self):
        if(self.ouputport):
            port = self.ouputport
            port.GetProducer().Update()
            return vtkAlgorithm.GetOutputDataObject(port.GetProducer(), port.GetIndex())
        else:
            raise ValueError("No producer ")


