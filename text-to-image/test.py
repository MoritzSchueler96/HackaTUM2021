from text_to_image import text_to_image, plot_images, save_images
import matplotlib.pyplot as plt

prompt = "cool geese"

imgs = text_to_image(prompt)

# plot_images(imgs)
save_images(imgs, prompt, folder="output/geese/", prefix="geese", summary=True)
