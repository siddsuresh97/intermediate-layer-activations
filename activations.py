from keras.applications.resnet50 import ResNet50
from keras.models import Model
from keras.preprocessing.image import img_to_array, load_img
import os
from tqdm import tqdm
from keras import backend as K
import pickle
from keras.preprocessing.image import ImageDataGenerator

def img_from_dir(dir):
    image_filenames  = [i for i in os.listdir(dir) if i[-1]=='g']
    X=[]
    for i in image_filenames:
        im = load_img(os.path.join(dir,i), target_size = (224,224))
        X.append(img_to_array(im))
    return X

def resnet(op_from_layers=[79]):
    model = ResNet50(include_top=True, weights='imagenet', input_tensor=None, input_shape=None)
    output_layers = [model.layers[i].output for i in op_from_layers]
    model_req = Model(input=model.input, output=output_layers)
    return model_req

def

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

def dump_pickle(reults):
    with open("results.p", 'wb') as pfile:
        pickle.dump(results, pfile, protocol=pickle.HIGHEST_PROTOCOL)

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
    parser.add_argument('--outputs_layers', nargs='+', type=int)


    args=parser.parse_args()

    directory = args.dir
    batch_size = args.batch_size
    height = args.input_height
    width = args.input_width
    output_from_layers = args.outputs_layers
    model = resnet(output_from_layers)
    results = prediction_with_flow(model, directory, batch_size, height, width)
    dump_pickle(results)

if __name__=="__main__":
    main()
