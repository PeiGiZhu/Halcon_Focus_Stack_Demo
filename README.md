# Halcon_Focus_Stack_Demo
A simple demo for Focus Stack using Halcon 20.11

### Running Environment

- OS: Windows 10

- Halcon: 20.11 Steady, Windows, Runtime Version

- Halcon/python: require python version >= 3.8

  ```python
  pip install mvtec-halcon==20111
  ```

- Installation Step: Check [here](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/products/halcon/documentation/manuals/installation_guide.pdf)

- Other dependencies:

  - numpy                    1.20.1
  - opencv-python      4.5.1.48

### Main Steps

- Align images(use opencv and numpy to align images)
- Decompose jpg images (with different focus level) into three types of single channel images (RGB). (halcon.decompose3(...) )
- Composes singal channel images into three stacks (three images). (halcon.append_channel(...) )
- Extract each pixels'depth on the three stacks. (halcon.depth_from_focus(...) )
- Selects R, G, B values (gray value) for each pixel in the final result image according to its depth from the previous step.(halcon.select_grayvalues_from_channels(...) )
- Recombine R, G, B image into jpg image.(halcon.append_channel(...) )

### Example
- Focus levels
  - ![image](https://raw.githubusercontent.com/PeiGiZhu/Halcon_Focus_Stack_Demo/main/input/step0.jpg)
  - ![image](https://raw.githubusercontent.com/PeiGiZhu/Halcon_Focus_Stack_Demo/main/input/step1.jpg)
  - ![image](https://raw.githubusercontent.com/PeiGiZhu/Halcon_Focus_Stack_Demo/main/input/step2.jpg)
  - ![image](https://raw.githubusercontent.com/PeiGiZhu/Halcon_Focus_Stack_Demo/main/input/step3.jpg)
  - ![image](https://raw.githubusercontent.com/PeiGiZhu/Halcon_Focus_Stack_Demo/main/input/step4.jpg)
  - ![image](https://raw.githubusercontent.com/PeiGiZhu/Halcon_Focus_Stack_Demo/main/input/step5.jpg)
- Result
  - ![image](https://raw.githubusercontent.com/PeiGiZhu/Halcon_Focus_Stack_Demo/main/SharpenedImage_ring.jpg)

### Referance

- python focus stack example (Align images functions) [reference](https://github.com/cmcguinness/focusstack)
- Halcon manual
  - [HALCON Operator Reference](https://www.mvtec.com/doc/halcon/2111/en/index.html)
  - [Solution Guide III-C 3D Vision](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/products/halcon/documentation/solution_guide/solution_guide_iii_c_3d_vision.pdf) 
