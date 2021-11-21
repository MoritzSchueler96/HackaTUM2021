from dalle_mini.model import CustomFlaxBartForConditionalGeneration
from transformers import BartTokenizer
import jax
import random
from vqgan_jax.modeling_flax_vqgan import VQModel
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

path = os.path.dirname(__file__)


def setup_model():
    # make sure we use compatible versions
    VQGAN_REPO = "flax-community/vqgan_f16_16384"
    VQGAN_COMMIT_ID = "90cc46addd2dd8f5be21586a9a23e1b95aa506a9"

    # make sure we use compatible versions
    DALLE_REPO = "flax-community/dalle-mini"
    DALLE_COMMIT_ID = "4d34126d0df8bc4a692ae933e3b902a1fa8b6114"

    # set up tokenizer and model
    tokenizer = BartTokenizer.from_pretrained(DALLE_REPO, revision=DALLE_COMMIT_ID)
    model = CustomFlaxBartForConditionalGeneration.from_pretrained(
        DALLE_REPO, revision=DALLE_COMMIT_ID
    )

    # set up VQGAN
    vqgan = VQModel.from_pretrained(VQGAN_REPO, revision=VQGAN_COMMIT_ID)

    return model, vqgan, tokenizer


def encode_images(prompt, model, tokenizer, n_predictions=9):
    # tokenize the prompt
    tokenized_prompt = tokenizer(
        prompt,
        return_tensors="jax",
        padding="max_length",
        truncation=True,
        max_length=128,
    )

    # create random keys
    seed = random.randint(0, 2 ** 32 - 1)
    key = jax.random.PRNGKey(seed)
    subkeys = jax.random.split(key, num=n_predictions)

    # generate sample predictions
    encoded_images = [
        model.generate(**tokenized_prompt, do_sample=True, num_beams=1, prng_key=subkey)
        for subkey in subkeys
    ]

    # remove first token (BOS)
    encoded_images = [img.sequences[..., 1:] for img in encoded_images]

    return encoded_images


def decode(encoded_images, vqgan):
    # decode images
    decoded_images = [
        vqgan.decode_code(encoded_image) for encoded_image in encoded_images
    ]

    # normalize images
    clipped_images = [img.squeeze().clip(0.0, 1.0) for img in decoded_images]

    # convert to image
    images = [
        Image.fromarray(np.asarray(img * 255, dtype=np.uint8)) for img in clipped_images
    ]

    return images


def text_to_image(prompt, n_predictions=9):

    model, vqgan, tokenizer = setup_model()
    enc_imgs = encode_images(prompt, model, tokenizer, n_predictions)
    images = decode(enc_imgs, vqgan)

    return images


def plot_images(images, prompt="", save=False):
    n = int(np.ceil(len(images) ** 0.5))
    for i, img in enumerate(images):
        plt.subplot(n, n, i + 1)
        plt.imshow(img, interpolation="none")
    plt.title(prompt)
    if save:
        plt.savefig("summary.png")


def save_images(images, prompt, folder=None, prefix="", summary=False):
    cwd = os.getcwd()
    os.chdir(path)
    if folder is not None:
        if not os.path.exists(os.path.join(cwd, folder)):
            os.makedirs(folder, exist_ok=True)
        os.chdir(folder)
    for i, img in enumerate(images):
        img.save(prefix + "_img_" + str(i) + ".png")
    if summary:
        plot_images(images, save=True)

    os.chdir(cwd)
