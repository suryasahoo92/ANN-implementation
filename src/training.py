from src.utils.common import read_config
from src.utils.data_mgmt import get_data
from src.utils.model import create_model, save_model, save_plot
from src.utils.callbacks import get_callbacks
import argparse
import os
import logging



def training(config_path):
    config = read_config(config_path)

    logging_str = "[%(asctime)s: %(levelname)s: %(module)s] %(message)s"
    LOG_DIR = config["logs"]['general_logs']
    log = config["logs"]["logs_dir"]
    GENERAL_LOGS_SAVE = os.path.join(log,LOG_DIR)
    os.makedirs(GENERAL_LOGS_SAVE, exist_ok=True)
    logging.basicConfig(filename= os.path.join(GENERAL_LOGS_SAVE,"running_logs.log"),level=logging.INFO, format=logging_str, filemode="a")
    

    validation_datasize = config["params"]["validation_datasize"]
    (X_train, y_train), (X_valid, y_valid), (X_test, y_test) = get_data(validation_datasize)

    LOSS_FUNCTION = config["params"]["loss_function"]
    OPTIMIZER = config["params"]["optimizer"]
    METRICS = config["params"]["metrics"]
    NUM_CLASSES = config["params"]["num_classes"]

    model = create_model(LOSS_FUNCTION, OPTIMIZER, METRICS, NUM_CLASSES)

    EPOCHS = config["params"]["epochs"]
    VALIDATION_SET = (X_valid, y_valid)

    CALLBACK_LIST = get_callbacks(config, X_train)

    history = model.fit(X_train, y_train, epochs=EPOCHS,
                    validation_data=VALIDATION_SET, callbacks=CALLBACK_LIST)

    artifacts_dir = config["artifacts"]["artifacts_dir"]
    model_dir = config["artifacts"]["model_dr"]

    model_dir_path = os.path.join(artifacts_dir, model_dir)
    os.makedirs(model_dir_path, exist_ok=True)
    model_name = config["artifacts"]["model_name"]
    save_model(model, model_name, model_dir_path)


    plot_dir = config["artifacts"]["plots_dir"]
    plot_dir_path = os.path.join(artifacts_dir, plot_dir)
    os.makedirs(plot_dir_path, exist_ok=True)
    plot_name = config["artifacts"]["plot_name"]
    loss_acc_plot = history.history
    save_plot(loss_acc_plot, plot_name, plot_dir_path)

if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument("--config", "-c", default="config.yaml")

    parsed_args = args.parse_args()
    try:
        logging.info(">>>>> starting training >>>>>")
        training(config_path=parsed_args.config)
        logging.info("<<<<< training done successfully<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e

    