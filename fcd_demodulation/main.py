import time
import os
from pathlib import Path

import matplotlib.pyplot as plt

from fcd_demodulation.select_roi import select_region
from fcd_demodulation.fcd import run_fcd
from fcd_demodulation.renderer import render


# constants
scale = 1 / 0.055
drop_diameter = 0.78
fluid_depth = 5
fluid_ior = 1.4009
acrylic_thickness = 5.7
acrylic_ior = 1.4906

# hstar formula: (1 - n_a/ n_l) * (h_l + (n_l / n_c)* h_c)
hstar = (1 - (1 / fluid_ior)) * (fluid_depth + (fluid_ior / acrylic_ior) * acrylic_thickness)

if __name__ == "__main__":
    import argparse
    
    start_time = time.time()

    # command line arguments
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument('output_folder', type=Path)
    argparser.add_argument('definition_folder_path', type=str)
    argparser.add_argument('definition_folder', type=Path)
    argparser.add_argument('-n', '--output_name', type=str, help='Name of output file')
    argparser.add_argument('-l', '--input_length', type=int, default=-1, help='number of files to process')
    argparser.add_argument('-1d', '--one_d', action='store_true')
    argparser.add_argument('-3d', '--three_d', action='store_true')

    args = argparser.parse_args()

    args.output_folder.mkdir(exist_ok=True)

    # user crop region
    crop_region = select_region(args.definition_folder)

    # render mode
    render_mode = 1 if args.one_d else 3 if args.three_d else 2

    # run fcd
    bins=16
    height_maps = run_fcd(args.reference_image_path, args.definition_folder_path,
                          None, scale, hstar, bins, debug=True)

    anim = render(height_maps, drop_diameter, scale, render_mode)

    image_extensions = (".png", ".jpg", ".jpeg", ".tif", ".tiff") 
    img_path = next((os.path.join(args.definition_folder, f) for f in os.listdir(args.definition_folder) if f.lower().endswith(image_extensions)), None)
    assert img_path is not None
    ani_name = args.output_name if args.output_name is not None else Path(img_path).stem
    output_path = args.output_folder.joinpath(f'{ani_name}.mp4')

    anim.save(output_path, writer='ffmpeg', fps=10)
    print(f'Total runtime {time.time() - start_time:.2f}s\n')
    
    plt.show()
