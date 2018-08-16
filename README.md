# intermediate-layer-activations

This repository helps you get activations from intermediate layers of a neural network on videos.
First step for doing an STA or STC.


Run the following commands:

1)python vid_to_frames.py --dir PATH/TO/DIR --ext '.mp4' --h 224 --w 224 --fps 50



2)python activations.py --dir PATH/TO/DIR --batch_size 32 --input_height 224 --input_width 224 --output_layers 79 --ouput_layers 80 --op_dir PATH/TO/OP/DIR --op_fname "results.h5"


    
