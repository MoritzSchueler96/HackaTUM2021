Either use text_to_image.py wrapper which uses DALLE mini or use vqgan

# DALLE Mini

# VQ GAN

To try out online:
https://replicate.ai/mehdidc/feed_forward_vqgan_clip

Git Repo:
https://github.com/mehdidc/feed_forward_vqgan_clip

For VQ GAN download the model and checkpoint file into the vqgan folder

For the model:

```
wget https://github.com/mehdidc/feed_forward_vqgan_clip/releases/download/0.2/cc12m_32x1024_vitgan.th
```

For the checkpoint:
https://github.com/mehdidc/feed_forward_vqgan_clip/releases/download/0.1/vqgan_imagenet_f16_16384.ckpt

To run:

```
python -u main.py test cc12m_32x1024_vitgan.th "Picture of a futuristic snowy city during the night, the tree is lit with a lantern"
```
