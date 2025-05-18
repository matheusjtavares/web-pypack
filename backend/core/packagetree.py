from abc import ABC, abstractmethod
import os
import shutil
from typing import List, Optional, Dict, Any
import zipfile
import shutil
import io

# Composite Design Pattern

class PackageComponent(ABC):
    '''Basic Component to be used for leafs and components '''
    def __init__(self, name: str):
        self.name:str = name
    
    @abstractmethod
    def generate(self, base_path: str) -> None:
        pass

# Leaf Component - Files
class PackageFile(PackageComponent):
    def __init__(self, name: str, content: str = ""):
        super().__init__(name) #Uses the package component init to define self.name
        self.content = content
    
    def generate(self, base_path: str) -> None:
        f = open(os.path.join(base_path,f"{self.name}.py"),"x")
        f.write(self.content)
        pass

# Node Component - Directories
class PackageDirectory(PackageComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: List[PackageComponent] = []
    
    def add(self, component: PackageComponent) -> 'PackageDirectory':
        self.children.append(component)
        print(f'{component.name} subfolder added to {self.name}')
        return self
    
    def generate(self, base_path: str) -> None:
        '''Generate folder structure recursively'''
        os.makedirs(f'{base_path}/{self.name}', exist_ok=True)
        while self.children!=[]:
             child = self.children.pop()
             child.generate(f'{base_path}/{self.name}')
        return
# Special composite for the root package
class Package(PackageDirectory):
    def __init__(self, name: str):
        super().__init__(name)
    
    def to_zip(self) -> bytes:
        """Convert package to ZIP file bytes"""
        memory_file = io.BytesIO()
        try:
            with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                temp_dir = os.path.join(os.path.dirname(__file__), "_temp_package")
                os.makedirs(temp_dir, exist_ok=True)
                self.generate(temp_dir)
                shutil.make_archive(f"outputs/teste/{self.name}", 'zip', os.path.join(temp_dir,self.name)) #debug only
        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
            
        memory_file.seek(0)
        return memory_file.getvalue()
            
    
