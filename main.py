import time
from pathlib import Path

from fcd_demodulation.select_roi import select_region
from fcd_demodulation.fcd import run_fcd
from fcd_demodulation.renderer import render

import matplotlib.pyplot as plt

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
    start_time = time.time()


    reference_image_path = 'C:/Users/gavin/Documents/Code/physicsthesis/checkerboard_sim/out/test1/reference.png'
    definition_folder_path = 'C:/Users/gavin/Documents/Code/physicsthesis/checkerboard_sim/out/test1/observed'
    bins = 1
    render_mode = 1

    height_maps = run_fcd(reference_image_path, definition_folder_path,
                          None, scale, hstar, bins, debug=True)

    anim = render(height_maps, drop_diameter, scale, render_mode)

    # image_extensions = (".png", ".jpg", ".jpeg", ".tif", ".tiff") 
    # img_path = next((os.path.join(definition_folder_path, f) for f in os.listdir(definition_folder_path) if f.lower().endswith(image_extensions)), None)
    # assert img_path is not None

    # ani_name = args.output_name if args.output_name is not None else Path(img_path).stem
    # output_path = args.output_folder.joinpath(f'{ani_name}.mp4')

    # anim.save(output_path, writer='ffmpeg', fps=10)


    print(f'Total runtime {time.time() - start_time:.2f}s\n')
    
    plt.show()
