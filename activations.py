from keras.applications.resnet50 import ResNet50
from keras.models import Model
from keras.preprocessing.image import img_to_array, load_img
import os
from tqdm import tqdm
from keras import backend as K
import pickle
from keras.preprocessing.image import ImageDataGenerator
import shutil

def resnet(op_from_layers=[79]):
    model = ResNet50(include_top=True, weights='imagenet', input_tensor=None, input_shape=None)
    output_layers = [model.layers[i].output for i in op_from_layers]
    model_req = Model(input=model.input, output=output_layers)
    return model_req

def prediction_with_flow(model,main_dir, batch_size, h, w):
    pred={}
    test_datagen = ImageDataGenerator()
    for i in tqdm(os.listdir(main_dir)):
        cwd = os.path.join(main_dir,i)
        if(os.path.isdir(cwd)):
            generator = test_datagen.flow_from_directory(
                    os.path.join(main_dir,i),
                    target_size = (h, w),
                    batch_size = batch_size)
            number_of_images = len(generator.filenames)
            probabilities = model.predict_generator(generator,steps=(number_of_images/batch_size)+1)
            pred.update({i.split("_")[0]:probabilities})
    return pred

def dump_pickle(results,output_dir):
    with open(os.path.join(output_dir,"results.p"), 'wb') as pfile:
        pickle.dump(results, pfile, protocol=pickle.HIGHEST_PROTOCOL)
        
def write_to_hdf5(results, op_fname, op_directory):
    dt = h5py.special_dtype(vlen=unicode)
    file = h5py.File(os.path.join(op_directory,op_fname),'w')
    file.create_dataset("fname", (len(results.keys()), dtype = dt)
    file.create_dataset("activations", results.keys()[0].shape, dtype = "f")
    for i in range(len(results.keys()):
        file['fname'][i] = results.keys()[0]
        file['activations'][i] = results[results.keys()[0]]
        
def put_dir_into_dir(directory):
    fnames = os.listdir(directory)
    for i in fnames:
        os.makedirs(os.path.join(directory,i+'_'))
        shutil.move(os.path.join(directory,i),os.path.join(directory,i+'_'))

def main():
    import argparse
    parser = argparse.ArgumentParser(description="  python blah blah  ")
    parser.add_argument('--dir',
                            type=str,
                            help="""full path to directory where the video is stored""")

    parser.add_argument('--batch_size',
                            type=int,
                            help="""batch_size of data""")
    parser.add_argument('--input_height',
                            type=int,
                            help="""height of input to the model""")

    parser.add_argument('--input_width',
                            type=int,
                            help="""width of input to the model""")
                   
    parser.add_argument('--output_layers', nargs='+', type=int)
                   
    parser.add_argument('--op_fname',
                            type=str,
                            help="""desired name of the output h5 file""")
                 
    parser.add_argument('--op_dir',
                            type=str,
                            help="""full path to desired output directory""")


    args=parser.parse_args()

    directory = args.dir
    batch_size = args.batch_size
    height = args.input_height
    width = args.input_width
    output_from_layers = args.output_layers
    op_fname = args.output_fname
    op_directory = args.op_dir
    model = resnet(output_from_layers)
    put_dir_into_dir(directory)
    results = prediction_with_flow(model, directory, batch_size, height, width)
    #dump_pickle(results,directory) use this if you want output from multiple layers or modify write_to_hdf5 
    import ipdb;ipdb.set_trace()
    write_to_hdf5(results, op_fname, op_directory)

if __name__=="__main__":
    main()
