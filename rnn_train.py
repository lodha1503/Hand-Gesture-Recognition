
import argparse
import tensorflow as tf
import tflearn
import os


def load_labels(label_file):
    label = {}
    count = 0
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label[l.strip()] = count
        count += 1
    return label


def main(input_data_dump, num_frames_per_video, batch_size, labels, model_file):
    # Get our data.
    X_train, X_test, y_train, y_test = get_data(input_data_dump, num_frames_per_video, labels, True)

    num_classes = len(labels)
    size_of_each_frame = X_train.shape[2]

    # Get our network.
    net = get_network_wide(num_frames_per_video, size_of_each_frame, num_classes)

    # Train the model.
    try:
        print("h1")
        model = tflearn.DNN(net, tensorboard_verbose=0)
        print("h2")
        model.load('C:/tmp/' + model_file)
        
        print("\nModel already exists! Loading it")
        print("Model Loaded")
    except Exception:
        print("h3")
        model = tflearn.DNN(net, tensorboard_verbose=0)
        print("\nNo previous checkpoints of %s exist" % (model_file))

    model.fit(X_train, y_train, validation_set=(X_test, y_test),
              show_metric=True, batch_size=batch_size, snapshot_step=100,
              n_epoch=10)

    # Save it.
    x = input("Do you wanna save the model and overwrite? y or n: ")
    if(x.strip().lower() == "y"):
        model.save('C:/tmp/' + model_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train a RNN')
    parser.add_argument("--input_file_dump", help="file containing intermediate representation of gestures from inception model",  default="C:/tmp/predicted-frames-final_result-train.pkl")
    parser.add_argument("--model_file", help="Name of the model file to be dumped. Model file is created inside a checkpoints folder", default="non_pool")
    parser.add_argument("--label_file", help="path to label file generated by inception", default="C:/tmp/output_labels.txt")
    parser.add_argument("--batch_size", help="batch Size", default=32)
    args = parser.parse_args("")

    labels = load_labels(args.label_file)
    input_data_dump = args.input_file_dump
    num_frames_per_video = 201
    batch_size = args.batch_size
    model_file = args.model_file

    main(input_data_dump, num_frames_per_video, batch_size, labels, model_file)