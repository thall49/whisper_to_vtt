import argparse
import warnings
# @Todo: remove this when numba is updated to 0.53.1
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")
import os
from tqdm import tqdm
import whisper
from whisper.utils import get_writer

class Transcriber:
    def __init__(self, directory, output, language_model, language, fp16):
        self.directory = directory
        self.output = output
        self.model = language_model
        self.language = language
        self.fp16 = fp16

    def batch_transcribe(self):
        for dirpath, dirnames, filenames in os.walk(self.directory):
            for filename in tqdm(filenames):
                self.__transcribe(os.path.join(self.directory, filename))
        return

    def __transcribe(self, file):
        model = whisper.load_model(self.model)
        result = model.transcribe(file, fp16=self.fp16, language=self.language)
        os.makedirs(self.output, exist_ok=True)
        output_file = f'{os.path.splitext(file)[0]}_{self.model}.vtt'
        writer = get_writer('vtt', self.output)
        writer(result, output_file)
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='Specify directory to files.', required=True)
    parser.add_argument('-o', '--output', help='Specify output directory', default='output')
    parser.add_argument('-m', '--model', help='Specify model', default='base',
                        choices=['tiny', 'base', 'small', 'medium', 'large'])
    parser.add_argument('-l', '--language', help='Specify language', default='English')
    parser.add_argument('-f', '--fp16', action='store_true', help='Use FP16 instead of FP32')
    args = parser.parse_args()
    x = Transcriber(args.directory, args.output, args.model, args.language, args.fp16)
    x.batch_transcribe()
